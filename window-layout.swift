import Cocoa
import ApplicationServices
let items:[(String,CGPoint,CGSize)] = [("com.factorio",CGPoint(x:0,y:30),CGSize(width:1024,height:960)),("com.openai.codex",CGPoint(x:1024,y:30),CGSize(width:683,height:960))]
for (id,origin,size) in items {
 guard let app=NSRunningApplication.runningApplications(withBundleIdentifier:id).first else {continue}
 let ax=AXUIElementCreateApplication(app.processIdentifier)
 var value:CFTypeRef?
 let result=AXUIElementCopyAttributeValue(ax,kAXWindowsAttribute as CFString,&value)
 guard result == .success, let wins=value as? [AXUIElement], !wins.isEmpty else {print(id,result.rawValue);continue}
 let win=wins.first(where: { w in var t:CFTypeRef?; AXUIElementCopyAttributeValue(w,kAXTitleAttribute as CFString,&t);return (t as? String ?? "") != "Window" }) ?? wins[0]
 var p=origin;var z=size
 print(id,AXUIElementSetAttributeValue(win,kAXPositionAttribute as CFString,AXValueCreate(.cgPoint,&p)!).rawValue,AXUIElementSetAttributeValue(win,kAXSizeAttribute as CFString,AXValueCreate(.cgSize,&z)!).rawValue)
}
