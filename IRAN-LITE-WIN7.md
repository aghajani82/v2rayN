# Iran Lite for Windows 7 SP1

This portable preview uses v2rayN 5.39, .NET Framework 4.8 and the official Windows 7 build of Xray 26.9.30. Windows 7 SP1 needs the updates listed by [XTLS](https://github.com/XTLS/go-win7), including KB4474419 and KB4490628. Use the package that matches the Windows system type.

Extract the ZIP into a fresh folder, run v2rayN.exe, import the normal subscription, select a server, and use System Proxy. The default Iran Lite profile keeps ChatGPT on the proxy and routes the shared Iranian domains and IPs directly. VLESS with XHTTP over TLS is supported in subscription imports.

To refresh the rules, close v2rayN and replace the two DAT files beside xray.exe with the [current rules](https://github.com/aghajani82/clashmi/tree/main/iran-lite). Relaunch v2rayN from the same directory to keep settings and subscriptions.

This is a compatibility preview for System Proxy. Native Windows 7 SP1 runtime testing is pending.

The package contains the Xray executable and the two routing assets. Start with `v2rayN.exe`.
