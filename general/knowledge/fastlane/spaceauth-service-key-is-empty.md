---
system: fastlane
status: verified
checked: 2026-09-14
tags: [fastlane, spaceauth, app-store-connect, apple-id, keychain]
---
# fastlane spaceauth fails with "Service key is empty"

## Symptom

`fastlane spaceauth -u <APPLE_ID>` (or any lane using Apple ID session login) prints, after the password prompt:

```
security: SecKeychainAddInternetPassword <NULL>: User interaction is not allowed
Could not store password in keychain
Service key is empty
Spaceship::AppleTimeoutError: Could not receive latest API key from App Store Connect
```

Affected: fastlane 2.238.0 and 2.239.0 (and older) as of September 2026.

## Cause

Apple removed the endpoint fastlane used to obtain `authServiceKey`:
`GET https://appstoreconnect.apple.com/olympus/v1/app/config?hostname=itunesconnect.apple.com`
now returns HTTP 404, so SIRP authentication cannot start. Upstream issue
`fastlane/fastlane#30199`; fix `fastlane/fastlane#30206` (commit `5bb425e`, merged 2026-09-12)
reads the key from the `widgetKey` in the redirect of `HEAD https://appstoreconnect.apple.com/logout`.
The fix ships in fastlane 2.240.0 (`fastlane/fastlane#30219`).

The Keychain message is a separate, local problem (headless/SSH session, locked login keychain).
It only prevents saving the password; it is not the cause of `Service key is empty`.

Quick check that you are hitting this (no secrets involved):

```bash
fastlane --version
curl -sS -o /dev/null -w 'olympus HTTP %{http_code}\n' \
  'https://appstoreconnect.apple.com/olympus/v1/app/config?hostname=itunesconnect.apple.com'
curl -sS -I -o /dev/null -w 'logout HTTP %{http_code}\n' 'https://appstoreconnect.apple.com/logout'
```

Expected in the broken state: `olympus HTTP 404`, `logout HTTP 302`, fastlane <= 2.239.0.

## Fix

Preferred: upgrade to fastlane >= 2.240.0 with a pinned `Gemfile.lock` and run `bundle exec fastlane ...`.

Until the release, use a temporary bundle pinned to the fixed commit, only to generate the session:

```ruby
source "https://rubygems.org"
gem "fastlane", git: "https://github.com/fastlane/fastlane.git", ref: "5bb425e"
```

```bash
bundle install
bundle exec fastlane spaceauth -u '<APPLE_ID>'
```

Generate the session on the same runner/region where it will be used and store it only in a masked,
protected CI variable `FASTLANE_SESSION`.

To bypass the Keychain in a headless session, provide the password through the environment without echo:

```zsh
read -s "FASTLANE_PASSWORD?Apple ID password: "; export FASTLANE_PASSWORD; echo
bundle exec fastlane spaceauth -u '<APPLE_ID>'
unset FASTLANE_PASSWORD
```

or unlock the login keychain with `security unlock-keychain ~/Library/Keychains/login.keychain-db`
(do not pass the password with `-p`, it would land in history and the process list).

## Limits

- Session auth remains dependent on 2FA and short-lived regional cookies; where the lane supports it,
  migrate to an App Store Connect API key instead.
- Remove the temporary git pin once the fixed gem is published.
