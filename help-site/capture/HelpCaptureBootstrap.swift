#if VIBEIT_HELP_CAPTURE
import Foundation
import UIKit

/// Capture-checkout-only credential handoff. This file is compiled only with the
/// explicit documentation flag, never into the regular release. It imports real,
/// already-authorized credentials; it does not inject provider health, model
/// catalogs, subscription entitlements, or successful-operation states.
@MainActor
enum HelpCaptureBootstrap {
    static func installIfRequested() {
        if ProcessInfo.processInfo.arguments.contains("--help-capture") { UIView.setAnimationsEnabled(false) }
        let documents = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let url = documents.appendingPathComponent(".help-import.json")
        guard let data = try? Data(contentsOf: url),
              let values = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
        defer { try? FileManager.default.removeItem(at: url) }
        if let token = values["githubToken"] as? String { PyDevSecretStore.githubToken = token }
        if let token = values["huggingFaceToken"] as? String { PyDevSecretStore.huggingFaceToken = token }
        if let token = values["claudeAPIKey"] as? String { PyDevSecretStore.claudeAPIKey = token }
        if let codex = values["codex"] as? [String: Any],
           let access = codex["access"] as? String,
           let expiry = codex["expiresAt"] as? TimeInterval,
           let account = codex["accountID"] as? String {
            PyDevSecretStore.storeCodexOAuthCredential(.init(access: access,
                                                           refresh: "",
                                                           expiresAt: Date(timeIntervalSince1970: expiry),
                                                           accountID: account,
                                                           email: nil))
        }
    }
}
#endif
