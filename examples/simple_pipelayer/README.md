# Simple PipeLayer App

## Running The App

Open a terminal and navigate to the project root directory.

Run this PowerShell script to setup the virtual environment:
```sh
.\scripts\setup-venv.ps1
```
Next, install the required packages:
```sh
.\scripts\install-reqs.ps1
```
Start the service:
```
python .\src\run.py
```
<br>

---

## Running The Service with The Debugger
If you're using VSCode and want to run the service with a debugger, open the workspace file found in the root directory of the project.

Hit `F5` or select `Start Debugging` from the `Run` menu.<br>
*(Make sure you've stopped the other instance that may still be running)*

Now any requests made from the Swagger UI will stop on any breakpoints you've set.<br><br>

*If you're using PyCharm, you're on your own getting the debugger configured. (for now)*
