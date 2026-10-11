# nordvik-azure – Hyresgästportal med felanmälan

Infrastruktur som kod (ARM) och app för Nordviks hyresgästportal. Fullständig rapport: [docs/rapport.md](docs/rapport.md).

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FHabibijoel%2Fnordvik-azure%2Fmain%2Fazuredeploy.json)

## Återskapa
1. Skapa resursgrupp `rg-nordvik` (Sweden Central).
2. Klicka **Deploy to Azure** ovan (eller Portal → *Deploy a custom template* → *Build your own template* → klistra in `azuredeploy.json`).
3. Välj `rg-nordvik`, behåll standardvärden eller ändra `storageAccountName`/`appName` (globalt unika). Valfritt: ange objectId för `SEC_Ekonomi`.
4. Review + create. Efter ca 5–10 min: öppna output `appUrl`.

## Innehåll
| Fil | Syfte |
|---|---|
| `azuredeploy.json` | ARM-mall: VNet, NSG, storage, private endpoint, privat DNS, App Service, hanterad identitet, RBAC |
| `azuredeploy.parameters.json` | Parametrar |
| `app/` | Flask-app (felanmälan: rubrik, beskrivning, bild) |
| `docs/rapport.md` | Rapport Del A + Del B |
