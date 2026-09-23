---
system: ios-ci
status: verified
checked: 2026-09-14
tags: [ios, fastlane, spaceauth, app-store-connect, apple-id, keychain, runner]
---
# YouDo iOS: fastlane `spaceauth` — `Service key is empty`

## Task

Explain why `fastlane spaceauth` fails with `Service key is empty` on the iOS runner `idcn-10` and how to regenerate the App Store Connect session.

## Context

- Investigation date: 2026-09-14
- Host according to the user's output: `idcn-10`, user `iosdev`
- Apple ID: corporate Apple Developer Program account (the address is not duplicated in this note)
- Command: `fastlane spaceauth -u <APPLE_ID>`

## Findings: symptom

After the password is entered fastlane reports:

- `security: SecKeychainAddInternetPassword <NULL>: User interaction is not allowed`;
- `Could not store password in keychain`;
- then `Service key is empty`;
- final result: `Spaceship::AppleTimeoutError: Could not receive latest API key from App Store Connect`.

## Findings: cause and boundaries of the problem

The confirmed primary cause of the login failure is a change on Apple's side. The endpoint
`GET https://appstoreconnect.apple.com/olympus/v1/app/config?hostname=itunesconnect.apple.com`,
from which fastlane obtained `authServiceKey`, started answering HTTP 404. Therefore Apple-ID/session login
in fastlane 2.238.0 and 2.239.0 cannot begin SIRP authentication. Upstream issue:
`https://github.com/fastlane/fastlane/issues/30199`.

The fix `fastlane/fastlane#30206` was merged on 2026-09-12 in commit `5bb425e`: the key is now read
from the `widgetKey` of the redirect of `HEAD https://appstoreconnect.apple.com/logout`, without cookies and without following
the redirect. As of 2026-09-14 the fix is in `master` but absent from the published gem 2.239.0;
release 2.240.0 is being prepared (`fastlane/fastlane#30219`).

The Keychain message is a separate local problem: the headless/SSH session did not allow interactive
access, or the login keychain is locked. It prevents the password from being saved, but it is not the cause of
`Service key is empty`: fastlane continues the login after this error and fails later on the Apple endpoint.

## Actions: diagnostics on the runner

The commands print no secrets:

```bash
fastlane --version
ruby -v
which fastlane
curl -sS -o /dev/null -w 'olympus HTTP %{http_code}\n' \
  'https://appstoreconnect.apple.com/olympus/v1/app/config?hostname=itunesconnect.apple.com'
curl -sS -I -o /dev/null -w 'logout HTTP %{http_code}\n' \
  'https://appstoreconnect.apple.com/logout'
```

For the described state the expected results are `olympus HTTP 404`, `logout HTTP 302` and fastlane no newer than
2.239.0.

## Findings: recovery

Preferably upgrade to fastlane 2.240.0 once it is published and run through a pinned
`Gemfile.lock`: `bundle exec fastlane ...`.

Until the release, a git version of fastlane pinned to the merge commit `5bb425e` can be used in a separate temporary bundle,
and only the session generation run through it. Example Gemfile entry:

```ruby
source "https://rubygems.org"
gem "fastlane", git: "https://github.com/fastlane/fastlane.git", ref: "5bb425e"
```

Then `bundle install` and `bundle exec fastlane spaceauth -u '<APPLE_ID>'`. The session must be generated
on the same runner/in the same region where it will be used. Store the session value only in a
protected masked CI variable `FASTLANE_SESSION`, not in Markdown or the repository.

To bypass the Keychain, the password can be read hidden into the current zsh session:

```zsh
read -s "FASTLANE_PASSWORD?Apple ID password: "; export FASTLANE_PASSWORD; echo
bundle exec fastlane spaceauth -u '<APPLE_ID>'
unset FASTLANE_PASSWORD
```

An alternative is to unlock the user's login keychain with
`security unlock-keychain ~/Library/Keychains/login.keychain-db`; do not pass the password with the `-p`
parameter so that it does not end up in history/process list.

If the lane in use supports the official App Store Connect API key, migrating to it is
preferable to session auth: no dependency on 2FA and short-lived regional cookies.

## Open items: TODO

- Check the actual fastlane version and installation method on `idcn-10`.
- After 2.240.0 is released, update the project's Gemfile/Gemfile.lock and remove the temporary git pin.
- Check which lanes still require an Apple-ID session and which can be moved to an App Store
  Connect API key.

## Portable lesson

- `~/ai/general/knowledge/fastlane/spaceauth-service-key-is-empty.md`
