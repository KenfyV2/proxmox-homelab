# ARR Stack

The ARR stack runs in VM 201 at `<ARR_IP>`.

## Components

### Seerr

Seerr is the user-facing request interface.

Users search for movies or TV shows and request them. Seerr does not download media itself.

It sends requests to:

- Radarr for movies
- Sonarr for TV shows

Local URL:

```text
http://<ARR_IP>:5055
```

Public URL:

```text
https://seer.kenfy.dev
```

---

### Radarr

Radarr manages movies.

Responsibilities:

- tracks requested movies
- searches for releases through Prowlarr
- applies quality and language profiles
- sends approved releases to SABnzbd
- imports completed downloads into `/data/media/movies`
- renames and organizes movie files
- monitors missing or upgraded releases

Local URL:

```text
http://<ARR_IP>:7878
```

Root folder:

```text
/data/media/movies
```

---

### Sonarr

Sonarr does the same job as Radarr, but for TV series.

Responsibilities:

- tracks shows and episodes
- monitors seasons/episodes
- searches through Prowlarr
- applies quality/language profiles
- sends releases to SABnzbd
- imports completed episodes into `/data/media/tv`
- organizes season folders and episode names

Local URL:

```text
http://<ARR_IP>:8989
```

Root folder:

```text
/data/media/tv
```

---

### Prowlarr

Prowlarr manages indexers.

Current primary indexer:

```text
NZBGeek
```

Prowlarr does not download files. It searches indexers and returns release information to Radarr and Sonarr.

Local URL:

```text
http://<ARR_IP>:9696
```

Prowlarr is routed through Gluetun.

---

### SABnzbd

SABnzbd is the actual Usenet downloader.

Provider:

```text
Newshosting
```

Responsibilities:

- accepts NZB jobs from Radarr/Sonarr
- downloads Usenet articles
- repairs/unpacks downloads
- places completed data into category folders
- reports completion/failure back to Radarr/Sonarr

Local URL:

```text
http://<ARR_IP>:8080
```

Folders:

```text
/data/usenet/incomplete
/data/usenet/complete/movies
/data/usenet/complete/tv
```

SABnzbd is routed through Gluetun.

---

### Gluetun

Gluetun provides the VPN network namespace.

Current VPN:

```text
PrivadoVPN
```

Only services that need the VPN are routed through it:

- SABnzbd
- Prowlarr

Radarr, Sonarr, Bazarr, and Seerr stay on the normal Docker network.

This is intentional because Radarr/Sonarr do not download copyrighted payload data themselves. They only coordinate and manage releases.

---

### Bazarr

Bazarr manages subtitles.

Current languages:

- English
- Japanese
- Korean

Current language profile:

```text
ENG + JPN + KOR
```

Current subtitle provider:

```text
OpenSubtitles.com
```

Bazarr integrates with:

- Radarr
- Sonarr
- Jellyfin

It watches imported media and searches for missing subtitle files.

Local URL:

```text
http://<ARR_IP>:6767
```

---

## Docker Networking

The stack uses Docker Compose.

Services such as Radarr and Sonarr can address each other by Docker service name:

```text
radarr:7878
sonarr:8989
```

SABnzbd and Prowlarr share Gluetun's network namespace.

For example, Radarr/Sonarr reach SABnzbd through:

```text
gluetun:8080
```

This is because SAB itself does not have a separate Docker network identity while using:

```yaml
network_mode: service:gluetun
```

## ARR Flow

```mermaid
flowchart LR
    User --> Seerr
    Seerr -->|Movie| Radarr
    Seerr -->|TV| Sonarr

    Radarr --> Prowlarr
    Sonarr --> Prowlarr

    Prowlarr --> NZBGeek

    Radarr --> SAB
    Sonarr --> SAB

    SAB --> Newshosting
    SAB --> Completed[Completed Download]

    Completed --> Radarr
    Completed --> Sonarr

    Radarr --> Movies[/data/media/movies]
    Sonarr --> TV[/data/media/tv]

    Movies --> Jellyfin
    TV --> Jellyfin

    Bazarr --> Movies
    Bazarr --> TV
```

## Failure Behavior

If SABnzbd cannot complete a release:

1. SAB reports failure.
2. Radarr/Sonarr marks that release as failed/blocklisted.
3. That exact release is not automatically selected again.
4. Radarr/Sonarr can search for another acceptable release.
5. Monitoring remains enabled unless the media was successfully imported and later intentionally deleted.

There is no simple fixed retry count. The system can continue trying different releases while the item remains monitored and matching releases are available.
