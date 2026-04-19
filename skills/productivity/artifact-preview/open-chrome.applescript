on run argv
    set rawMode to "full"
    if (count of argv) > 0 then set rawMode to item 1 of argv

    try
        set theMode to do shell script "printf %s " & quoted form of rawMode & " | tr '[:upper:]' '[:lower:]' | tr -d \"'\" | xargs"
    on error
        set theMode to rawMode
    end try

    set previewURL to "http://localhost:8765"

    -- Ensure Chrome is running — use "open" to respect default profile
    tell application "System Events"
        set chromeRunning to (exists (processes where name is "Google Chrome"))
    end tell

    if not chromeRunning then
        do shell script "open -a 'Google Chrome'"
        delay 1.0
    end if

    tell application "Google Chrome"
        activate

        try
            make new window
            delay 0.15
            set URL of active tab of front window to previewURL

            if theMode is "portrait" then
                set bounds of front window to {60, 60, 490, 904}
            else if theMode is "horizontal" then
                set bounds of front window to {60, 60, 1300, 740}
            else
                -- full: get main screen logical size and set window bounds
                set screenDims to do shell script "swift -e 'import AppKit; let s = NSScreen.main!.frame.size; print(Int(s.width), Int(s.height))'"
                set oldDelims to AppleScript's text item delimiters
                set AppleScript's text item delimiters to " "
                set screenW to (text item 1 of screenDims) as integer
                set screenH to (text item 2 of screenDims) as integer
                set AppleScript's text item delimiters to oldDelims
                set bounds of front window to {0, 0, screenW, screenH}
            end if

        on error errMsg number errNum
            delay 0.5
            try
                make new window
                delay 0.15
                set URL of active tab of front window to previewURL
                if theMode is "portrait" then
                    set bounds of front window to {60, 60, 490, 904}
                else if theMode is "horizontal" then
                    set bounds of front window to {60, 60, 1300, 740}
                else
                    set screenDims to do shell script "swift -e 'import AppKit; let s = NSScreen.main!.frame.size; print(Int(s.width), Int(s.height))'"
                    set oldDelims to AppleScript's text item delimiters
                    set AppleScript's text item delimiters to " "
                    set screenW to (text item 1 of screenDims) as integer
                    set screenH to (text item 2 of screenDims) as integer
                    set AppleScript's text item delimiters to oldDelims
                    set bounds of front window to {0, 0, screenW, screenH}
                end if
            on error errMsg2 number errNum2
                do shell script "printf 'Fatal: %s (%d)\\n' " & quoted form of errMsg2 & " " & errNum2 & " >&2; exit 4"
            end try
        end try
    end tell
end run
