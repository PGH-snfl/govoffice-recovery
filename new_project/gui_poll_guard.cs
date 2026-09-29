// Keep PowerShell timer callbacks out of Windows' native move/size loop.
// No document access, worker waits, UI updates or script callbacks in this hook.
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Interop;

public static class GovOfficePollGuard
{
    private static readonly HashSet<IntPtr> moving = new HashSet<IntPtr>();
    private static readonly HashSet<IntPtr> attached = new HashSet<IntPtr>();
    private static bool initialized;
    private static int pauseCount;
    public static bool IsPaused { get { return pauseCount > 0; } }
    public static bool IsMoving { get { return moving.Count != 0; } }

    public static IDisposable Pause()
    {
        System.Threading.Interlocked.Increment(ref pauseCount);
        return new PauseScope();
    }
    private sealed class PauseScope : IDisposable
    {
        private int disposed;
        public void Dispose()
        {
            if (System.Threading.Interlocked.Exchange(ref disposed, 1) == 0)
                System.Threading.Interlocked.Decrement(ref pauseCount);
        }
    }

    public static void Initialize()
    {
        if (initialized) return;
        initialized = true;
        EventManager.RegisterClassHandler(typeof(Window), FrameworkElement.LoadedEvent,
            new RoutedEventHandler(OnLoaded));
    }

    private static void OnLoaded(object sender, RoutedEventArgs args)
    {
        Window window = sender as Window;
        if (window == null || !Object.ReferenceEquals(args.OriginalSource, window)) return;
        IntPtr handle = new WindowInteropHelper(window).Handle;
        HwndSource source = HwndSource.FromHwnd(handle);
        if (source != null && attached.Add(handle)) source.AddHook(OnMessage);
    }

    private static IntPtr OnMessage(IntPtr hwnd, int message, IntPtr wParam, IntPtr lParam, ref bool handled)
    {
        if (message == 0x0231) moving.Add(hwnd); // WM_ENTERSIZEMOVE
        if (message == 0x0232) moving.Remove(hwnd); // WM_EXITSIZEMOVE
        if (message == 0x0082) // WM_NCDESTROY: an interrupted move must not lock polling
        {
            moving.Remove(hwnd);
            attached.Remove(hwnd);
        }
        return IntPtr.Zero;
    }

    public static EventHandler Wrap(EventHandler callback)
    {
        if (callback == null) throw new ArgumentNullException("callback");
        return delegate(object sender, EventArgs args)
        {
            // Gate BEFORE invoking the PowerShell delegate, not inside it.
            if (!IsMoving && !IsPaused) callback(sender, args);
        };
    }
}
