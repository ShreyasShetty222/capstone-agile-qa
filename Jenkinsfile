pipeline {
  agent any
  options { timestamps() }
  environment {
    AVD_NAME = "Medium_Phone_API_36.1"   // <- change if your AVD name differs
    PY = "py"                            // or "python" if py launcher not present
  }
  stages {
    stage("Checkout") {
      steps { checkout scm }
    }
    stage("Python venv & deps") {
      steps {
        bat """
        %PY% -3 -m venv .venv
        .venv\\Scripts\\python -m pip install --upgrade pip
        .venv\\Scripts\\pip install -r requirements.txt
        """
      }
    }
    stage("Start Emulator") {
      steps { powershell 'ci/start_emulator.ps1 -AvdName "$env:AVD_NAME"' }
    }
    stage("Start Appium (bg)") {
      steps {
        bat 'start "" cmd /c appium --address 127.0.0.1 --port 4723 --allow-insecure="*:chromedriver_autodownload"'
        bat 'ping 127.0.0.1 -n 6 >NUL'
      }
    }
    stage("Run tests (web + mobile)") {
      steps { bat '.venv\\Scripts\\pytest -q --alluredir=reports\\allure-results' }
    }
    stage("Allure Report") {
      steps { allure([ results: [[ path: "reports/allure-results" ]] ]) }
    }
  }
  post {
    always {
      powershell 'ci/stop_emulator.ps1'
      archiveArtifacts artifacts: "reports/**", fingerprint: true, onlyIfSuccessful: false
    }
  }
}
