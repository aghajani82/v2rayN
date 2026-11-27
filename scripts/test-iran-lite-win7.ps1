param([Parameter(Mandatory)][string] $Stage)

$ErrorActionPreference = 'Stop'
Set-Location $Stage
[Environment]::CurrentDirectory = $Stage
@'
using System;
using System.IO;
using System.Reflection;

class Smoke
{
    public static void Main()
    {
        var app = Assembly.LoadFrom("v2rayN.exe");
        var config = app.GetType("v2rayN.Handler.ConfigHandler", true);
        var share = app.GetType("v2rayN.Handler.ShareHandler", true);
        var core = app.GetType("v2rayN.Handler.V2rayConfigHandler", true);
        var arguments = new object[] { null };
        if ((int)config.GetMethod("LoadConfig").Invoke(null, arguments) != 0 ||
            (int)config.GetMethod("InitBuiltinRouting").Invoke(null, new object[] { arguments[0], false }) != 0)
        {
            throw new InvalidOperationException("Could not load the Iran Lite profile");
        }

        const string link = "vless://a3482e88-686a-4a58-8126-99c9df64b7bf@example.com:443?encryption=none&security=tls&alpn=h2&type=xhttp&host=example.com&path=%2Fexample%2F&mode=stream-up&extra=%7B%22noGRPCHeader%22%3Atrue%7D#Smoke";
        var node = share.GetMethod("ImportFromClipboardConfig").Invoke(null, new object[] { link, "" });
        arguments = new object[] { node, null, "", "" };
        if ((int)core.GetMethod("GenerateClientConfig").Invoke(null, arguments) != 0)
        {
            throw new InvalidOperationException("XHTTP config generation failed: " + arguments[2]);
        }
        File.WriteAllText("smoke.json", (string)arguments[3]);
    }
}
'@ | ForEach-Object { Add-Type -TypeDefinition $_ -Language CSharp -OutputType ConsoleApplication -OutputAssembly (Join-Path $Stage 'smoke.exe') }
try {
    & (Join-Path $Stage smoke.exe)
    if ($LASTEXITCODE -ne 0) { throw 'Config generation failed' }
    $generated = Get-Content smoke.json -Raw | ConvertFrom-Json
    $proxy = $generated.outbounds | Where-Object tag -eq proxy
    $xhttp = $proxy.streamSettings.xhttpSettings
    if ($proxy.streamSettings.network -ne 'xhttp' -or $xhttp.path -ne '/example/' -or
        $xhttp.mode -ne 'stream-up' -or $xhttp.extra.noGRPCHeader -ne $true -or
        $generated.routing.domainStrategy -ne 'IPOnDemand') {
        throw 'XHTTP or Iran Lite routing settings were lost'
    }
    $rules = $generated.routing.rules
    $proxyFirst = [array]::FindIndex([object[]] $rules, [Predicate[object]] { param($r) $r.domain -contains 'domain:chatgpt.com' })
    $directAfter = [array]::FindIndex([object[]] $rules, [Predicate[object]] { param($r) $r.domain -contains 'ext:iran-lite-domains.dat:ir' })
    if ($proxyFirst -lt 0 -or $directAfter -le $proxyFirst) {
        throw 'Iran Lite routing order is wrong'
    }
    & (Join-Path $Stage xray.exe) run -test -config smoke.json
    if ($LASTEXITCODE -ne 0) { throw 'Xray rejected the generated configuration' }
} finally {
    Remove-Item smoke.exe, smoke.json, guiNConfig.json -ErrorAction SilentlyContinue
}
