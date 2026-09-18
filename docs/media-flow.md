# Media Request Flow

## Movie Example

A user requests a movie in Seerr.

```text
Seerr
  ↓
Radarr
  ↓
Prowlarr
  ↓
NZBGeek
  ↓
Radarr chooses a matching release
  ↓
SABnzbd
  ↓
Newshosting
  ↓
Download + unpack
  ↓
Radarr imports movie
  ↓
/data/media/movies
  ↓
Jellyfin scan
  ↓
Movie appears in Jellyfin
```

## TV Example

```text
Seerr
  ↓
Sonarr
  ↓
Prowlarr
  ↓
NZBGeek
  ↓
Sonarr chooses release
  ↓
SABnzbd
  ↓
Newshosting
  ↓
Download + unpack
  ↓
Sonarr imports episode
  ↓
/data/media/tv
  ↓
Jellyfin scan
  ↓
Episode appears in Jellyfin
```

## Subtitle Flow

```text
Radarr / Sonarr import media
       ↓
Bazarr sees new media
       ↓
Bazarr checks subtitle profile
       ↓
OpenSubtitles.com
       ↓
Subtitle downloaded beside media
       ↓
Jellyfin metadata refresh
       ↓
Subtitle becomes selectable
```

## Request Profiles

Language-related profiles were created so users can request different preferred release types.

Examples:

```text
HD-1080p - English
HD-1080p - Japanese
HD-1080p - Korean
HD-1080p - Original
```

Custom formats can prefer releases containing combinations such as:

```text
English + Japanese
English + Korean
English Dub
```

Anime release naming is inconsistent, so minimum custom format scores should not be set so aggressively that valid multi-language releases are rejected solely because the release title does not match a regex.

## Deletion Flow

The preferred deletion workflow is:

```text
Delete media in Jellyfin
        ↓
Actual file is removed
        ↓
Radarr/Sonarr refresh
        ↓
Missing file is detected
        ↓
Item is unmonitored
```

Relevant settings:

```text
Radarr: Unmonitor Deleted Movies = ON
Sonarr: Unmonitor Deleted Episodes = ON
```

This prevents intentionally deleted media from automatically being downloaded again.

Normal users should not receive media-deletion permission in Jellyfin. Keep deletion for the administrator account.
