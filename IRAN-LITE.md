# Aghajani Edition — Iran Lite (Windows)

On a fresh Windows configuration, the app selects **Aghajani Edition - Iran Lite**.
Import a subscription, select a node, and turn on System Proxy when you want the
system's proxy-aware applications to use that node. Use a new extracted folder
without a previous `guiConfigs` directory to test factory defaults.

The profile sends the Iranian domain list and Iranian IP ranges directly. The
remaining traffic goes through the selected proxy. On Xray, ChatGPT and its
connection dependencies use the proxy before Iran destination rules are checked. It includes `.ir`, `.ایران`,
Iranian chat and payment domains, and the IranServer ranges. Generic malware,
phishing, cryptomining, and adult-content categories are not used as direct rules.
Existing routing profiles and regional presets remain available. The app does not
import any subscriptions or credentials by default.

The rule data is embedded for offline startup. The source lists are
[Chocolate4U/Iran-v2ray-rules](https://github.com/Chocolate4U/Iran-v2ray-rules) (GPLv3)
and [bootmortis/iran-hosted-domains](https://github.com/bootmortis/iran-hosted-domains)
(MIT). To regenerate the asset, update the release URLs and SHA-256 digests in
`scripts/generate-iran-lite-routing.py` and run it with Python 3.

## bootmortis MIT notice

Copyright (c) 2022 bootmortis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
