on run argv
    set rawMode to "full"
    if (count of argv) > 0 then set rawMode to item 1 of argv

    try
        set theMode to do shell script "printf %s " & quoted form of rawMode & " | tr '[:upper:]' '[:lower:]' | tr -d \"'\" | xargs"
    on error
        set theMode to rawMode
    end try

    set previewURL to "http://localhost:8765"

    tell application "System Events"
        set chromeRunning to (exists (processes where name is "Google Chrome"))
    end tell

    set didColdStart to false

    if not chromeRunning then
        do shell script "open -a 'Google Chrome' --args --profile-directory=Default " & quoted form of previewURL
        delay 2.0
        set didColdStart to true
    end if

    tell application "Google Chrome"
        if didColdStart is false then
            activate
            make new window
            delay 0.15
            set URL of active tab of front window to previewURL
        end if

        delay 0.1

        if theMode is "portrait" then
            set bounds of front window to {60, 60, 510, 860}
        else if theMode is "horizontal" then
            set bounds of front window to {60, 60, 1340, 780}
        else
            set screenDims to do shell script "swift -e 'import AppKit; let s = NSScreen.main!.frame.size; print(Int(s.width), Int(s.height))'"
            set oldDelims to AppleScript's text item delimiters
            set AppleScript's text item delimiters to " "
            set screenW to (text item 1 of screenDims) as integer
            set screenH to (text item 2 of screenDims) as integer
            set AppleScript's text item delimiters to oldDelims
            set bounds of front window to {0, 0, screenW, screenH}
        end if

        activate
    end tell
end run
