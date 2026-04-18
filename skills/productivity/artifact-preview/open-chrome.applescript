on run argv
    set rawMode to "full"
    if (count of argv) > 0 then set rawMode to item 1 of argv

    -- Normalize: lowercase, strip whitespace
    try
        set mode to do shell script "printf %s " & quoted form of rawMode & " | tr '[:upper:]' '[:lower:]' | tr -d \"'\" | xargs"
    on error
        set mode to rawMode
    end try

    set previewURL to "http://localhost:8765"

    -- Ensure Chrome is running
    tell application "System Events"
        set chromeRunning to (exists (processes where name is "Google Chrome"))
    end tell

    if not chromeRunning then
        tell application "Google Chrome" to launch
        delay 0.6
    end if

    tell application "Google Chrome"
        activate

        try
            make new window
            delay 0.15

            if mode is "portrait" then
                set bounds of front window to {60, 60, 490, 904}
            else if mode is "horizontal" then
                set bounds of front window to {60, 60, 1300, 740}
            else
                -- full: use primary display bounds
                tell application "Finder"
                    set screenBounds to bounds of window of desktop
                end tell
                set bounds of front window to screenBounds
            end if

            set URL of active tab of front window to previewURL

        on error errMsg number errNum
            -- Attempt recovery: quit, relaunch, retry once
            try
                tell application "Google Chrome" to quit
            end try
            delay 0.6
            try
                tell application "Google Chrome" to launch
                delay 0.8
                tell application "Google Chrome" to activate
                make new window
                if mode is "portrait" then
                    set bounds of front window to {60, 60, 490, 904}
                else if mode is "horizontal" then
                    set bounds of front window to {60, 60, 1300, 740}
                else
                    tell application "Finder"
                        set screenBounds to bounds of window of desktop
                    end tell
                    set bounds of front window to screenBounds
                end if
                set URL of active tab of front window to previewURL
            on error errMsg2 number errNum2
                do shell script "printf 'Fatal: %s (%d)\n' " & quoted form of errMsg2 & " " & errNum2 & " >&2; exit 4"
            end try
        end try
    end tell
end run
