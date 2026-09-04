using System;
using System.IO;
using System.Management.Automation;
using System.Management.Automation.Runspaces;
using System.Threading;

internal static class GovOfficePreviewHost
{
    [STAThread]
    private static int Main(string[] args)
    {
        var requestedScript = args.Length == 0
            ? Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "launch_gui.ps1")
            : args[0];
        if (!File.Exists(requestedScript))
        {
            return 2;
        }

        Environment.SetEnvironmentVariable("GOVOFFICE_LAYOUT_PREVIEW", "1");
        Environment.SetEnvironmentVariable("GOVOFFICE_LAYOUT_PREVIEW_TAB", "개인");
        for (var index = 1; index + 1 < args.Length; index += 2)
        {
            if (args[index] == "--tab")
            {
                Environment.SetEnvironmentVariable("GOVOFFICE_LAYOUT_PREVIEW_TAB", args[index + 1]);
            }
            else if (args[index] == "--surface")
            {
                Environment.SetEnvironmentVariable("GOVOFFICE_LAYOUT_PREVIEW_SURFACE", args[index + 1]);
            }
        }

        var scriptPath = Path.GetFullPath(requestedScript);
        var projectDirectory = Path.GetDirectoryName(scriptPath);
        Directory.SetCurrentDirectory(projectDirectory);
        Environment.SetEnvironmentVariable("GOVOFFICE_PROJECT_DIR", projectDirectory);
        var sessionState = InitialSessionState.CreateDefault();
        sessionState.ExecutionPolicy = Microsoft.PowerShell.ExecutionPolicy.Bypass;
        using (var runspace = RunspaceFactory.CreateRunspace(sessionState))
        {
            runspace.ApartmentState = ApartmentState.STA;
            runspace.ThreadOptions = PSThreadOptions.ReuseThread;
            runspace.Open();
            using (var shell = PowerShell.Create())
            {
                shell.Runspace = runspace;
                shell.AddScript(File.ReadAllText(scriptPath));
                shell.Invoke();
                if (!shell.HadErrors)
                {
                    return 0;
                }

                var logPath = Path.Combine(Path.GetDirectoryName(scriptPath), "reports", "runtime", "preview_host_errors.log");
                Directory.CreateDirectory(Path.GetDirectoryName(logPath));
                using (var writer = new StreamWriter(logPath, true))
                {
                    foreach (var error in shell.Streams.Error)
                    {
                        writer.WriteLine(error.ToString());
                    }
                }
                return 1;
            }
        }
    }
}
