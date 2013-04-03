import os
import sys

import servicemanager
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil

from system import *

class WinService(win32serviceutil.ServiceFramework):

    _svc_name_ = "PythonAboard"
    _svc_display_name_ = "Python Aboard servers"
    _svc_description_ = "This service manages the Python Aboard servers."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.executable_command = get_executable_command()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """The service is actually running."""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, ''))
        self.timeout = 10000 #  10 seconds
        while True:
            # Wait for service stop signal, otherwise wait and continue
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)

            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("{}- STOPPED!".format(
                        self._svc_display_name_))
                self.stop_servers()
                break
            else:
                # Check that the servers are started and, if not,
                # launch them
                try:
                    self.check_and_launch_servers()
                except Exception as err:
                    pass

    def check_and_launch_servers(self):
        """Check that the specified servers are running.

        If they are not, launch them in a separate process.

        The servers are listed in the servers.txt file (a server per
        line).  The first line should be the direcotry leading to the
        administrator's website, if it ever exists.

        """
        lines = self.read_server_config()
        for line in lines:
            self.check_and_launch_server(line)

    def check_and_launch_server(self, path):
        """Launch the server.

        The given path is the configuration one.  Then the first check
        is the path existence.  If the path does exist, then try to
        read the '{path}/tmp/pid' file.  If it can be read and the
        PID does exist, the server is not launched.  But if the file
        doesn't exist (or contain a PID that doesn't exist), the
        server is launched.

        """
        if os.path.exists(path):
            pid = self.get_pid_for(path)
            if pid and is_process_running(pid):
                return

            cmd = "start " + self.executable_command
            cmd += " start server --path " + path
            os.system(cmd)

    def stop_servers(self):
        """Stop all configured servers."""
        lines = self.read_server_config()
        for line in lines:
            pid = self.get_pid_for(line)
            if pid and is_process_running(pid):
                stop_process(pid)

    def get_pid_for(self, path):
        """Try to find the PID for the path.

        Note: even if the PID is found in the {path}/tmp/pid file,
        that doesn't mean that this process is running.  Anyway, if
        the path is not found, return None.

        """
        pid_file = os.path.join(path, "tmp", "pid")
        pid = None
        if os.path.exists(pid_file):
            with open(pid_file, "r") as file:
                pid = file.read()

        return pid

    def read_server_config(self):
        """Read and return the server's configuration."""
        source = get_source_directory()
        config_path = os.path.join(source, "servers.txt")
        lines = []
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                content = file.read()

            lines = content.split("\n")

        return lines

def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(WinService)
