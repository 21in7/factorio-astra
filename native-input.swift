import AppKit
import CoreGraphics
let args = CommandLine.arguments
let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.factorio")
let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly,.excludeDesktopElements], kCGNullWindowID) as? [[String:Any]] ?? []
let found = windows.filter{ ($0[kCGWindowOwnerName as String] as? String ?? "").lowercased().contains("factorio") }
if args.count < 2 || args[1] == "windows" { for w in found { print(w) }; exit(0) }
guard let win=found.first(where: { ($0[kCGWindowName as String] as? String ?? "").hasPrefix("Factorio") }), let pid=win[kCGWindowOwnerPID as String] as? Int32, let bounds=win[kCGWindowBounds as String] as? [String:Double] else { exit(1) }
NSRunningApplication(processIdentifier:pid)?.activate(options: [.activateIgnoringOtherApps])
Thread.sleep(forTimeInterval:0.7)
print("front", NSWorkspace.shared.frontmostApplication?.localizedName ?? "none")
let src=CGEventSource(stateID:.hidSystemState)
if args[1] == "click" {
 let p=CGPoint(x: bounds["X"]!+Double(args[2])!, y:bounds["Y"]!+Double(args[3])!)
 CGEvent(mouseEventSource:src,mouseType:.mouseMoved,mouseCursorPosition:p,mouseButton:.left)?.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.08)
 CGEvent(mouseEventSource:src,mouseType:.leftMouseDown,mouseCursorPosition:p,mouseButton:.left)?.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.12)
 CGEvent(mouseEventSource:src,mouseType:.leftMouseUp,mouseCursorPosition:p,mouseButton:.left)?.post(tap:.cghidEventTap)
} else if args[1] == "release" {
 for code:CGKeyCode in [0,1,2,13,49] {
  CGEvent(keyboardEventSource:src,virtualKey:code,keyDown:false)?.post(tap:.cghidEventTap)
 }
 Thread.sleep(forTimeInterval:0.15)
} else if args[1] == "key" {
 let code=CGKeyCode(args[2])!
 CGEvent(keyboardEventSource:src,virtualKey:code,keyDown:true)?.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval: args.count>3 ? Double(args[3])! : 0.12)
 CGEvent(keyboardEventSource:src,virtualKey:code,keyDown:false)?.post(tap:.cghidEventTap)
} else if args[1] == "unicode" {
 for ch in args[2].utf16 {
  var c=ch
  let down=CGEvent(keyboardEventSource:src,virtualKey:0,keyDown:true)!
  down.keyboardSetUnicodeString(stringLength:1,unicodeString:&c);down.post(tap:.cghidEventTap)
  Thread.sleep(forTimeInterval:0.005)
  let up=CGEvent(keyboardEventSource:src,virtualKey:0,keyDown:false)!
  up.keyboardSetUnicodeString(stringLength:1,unicodeString:&c);up.post(tap:.cghidEventTap)
  Thread.sleep(forTimeInterval:0.005)
 }
} else if args[1] == "text" {
 let board=NSPasteboard.general; let old=board.string(forType:.string)
 board.clearContents(); board.setString(args[2],forType:.string)
 let mod=CGEvent(keyboardEventSource:src,virtualKey:55,keyDown:true)!;mod.flags = .maskCommand;mod.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.08)
 let down=CGEvent(keyboardEventSource:src,virtualKey:9,keyDown:true)!;down.flags = .maskCommand;down.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.15)
 let up=CGEvent(keyboardEventSource:src,virtualKey:9,keyDown:false)!;up.flags = .maskCommand;up.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.08)
 CGEvent(keyboardEventSource:src,virtualKey:55,keyDown:false)?.post(tap:.cghidEventTap)
 Thread.sleep(forTimeInterval:0.3)
 board.clearContents(); if let old=old {board.setString(old,forType:.string)}
}
