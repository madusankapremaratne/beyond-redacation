// UIDeviceInfo.swift -- small wrapper so BenchmarkRunner doesn't import UIKit directly.

import UIKit

struct UIDeviceInfo {
    let osVersion: String
    let model: String

    static func current() -> UIDeviceInfo {
        let device = UIDevice.current
        return UIDeviceInfo(osVersion: device.systemVersion, model: device.model)
    }
}
