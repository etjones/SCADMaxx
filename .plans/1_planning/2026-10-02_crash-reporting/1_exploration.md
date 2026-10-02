# SCADMaxx crash reporting

Status: planning feature; implementation and service selection have not been approved.
Created: 2026-10-02, from the chat "Assess SCADMaxx crash reporting".
Chat ID: `01a0f95e-632f-7772-aaf1-3e1140bf0e47`.

## Purpose

Collect useful native crash reports from distributed SCADMaxx builds, identify the exact affected build,
group repeated crashes, and turn actionable groups into GitHub issues.

The user requested an assessment of integration effort, suitable reporters, collector hosting, GitHub integration
and free open-source plans, then asked to retain that discussion as a planning feature. This document records
proposals, not a decision to implement, create accounts, apply for sponsorship, publish source or enable uploads.

## Proposed starting point

Evaluate Sentry Native with the Crashpad backend and hosted Sentry first. Target the existing Windows x64
C++/Qt/CMake distribution initially. BugSplat is a strong alternative with explicit Qt support.

| Option | Assessment |
| --- | --- |
| Sentry Native + hosted Sentry | Preferred initial candidate; native capture, analysis and GitHub integration. |
| BugSplat | Desktop-focused alternative with Qt/C++ support and GitHub issue creation. |
| Self-hosted Sentry | More hosting control, with server maintenance, backups, upgrades and storage overhead. |
| Crashpad + custom collector | Flexible, but requires building or integrating analysis, grouping and issue routing. |

Prefer a hosted collector for the first version. A custom collector is not needed solely to receive reports.
The full self-hosted Sentry installation was documented at roughly 16 GB host RAM and four CPUs during research;
an errors-only profile has lower requirements. Recheck deployment requirements before provisioning.

## Proposed scope

- Initialize native crash capture early and include the external handler in the distributed ZIP.
- Tag reports with the immutable experimental run ID, final source SHA, rendering backend and relevant features.
- Record bounded operation breadcrumbs such as preview, render and export, without attaching model contents by default.
- Provide explicit upload consent/control, writable local pending-report storage and offline retry behavior.
- Generate, retain and upload matching PDB symbols for every distributed optimized Windows build.
- Group equivalent crashes and initially let a maintainer review groups before creating GitHub issues.
- Later consider automatic issue creation for new groups or groups crossing a frequency threshold.
- Keep raw dumps private; publish only a suitable summary and report link to the selected GitHub repository.

Raw minidumps can contain memory fragments, paths and model data even without explicit source attachments.
Consent, collected metadata, retention and access therefore need concrete design before implementation.
Freezes, forced termination and GPU resets are not all ordinary process crashes; hang reporting is separate scope.

## Build and workspace integration

The build script inspected in the original assessment selected Release and had no explicit symbol-upload step.
Preserve optimization while producing matching symbols; do not substitute symbols from a later rebuild.
Assess symbol availability for shipped dependencies as well as the application.

Use the existing release identity and immutable build records to associate reports, binaries, symbols and source.
Relevant control files are `experimental/scripts/Build-Windows.ps1`, `experimental/profiles/windows-x64.md`,
`experimental/versioning-and-releases.md` and `workflows/update-and-build-scadmaxx.md`.

Keep the reporting endpoint configurable and keep symbol-upload credentials and GitHub write credentials out of
the application. Plan SDK dependencies under the shared-dependency policy rather than installing them implicitly.
Before implementation, inspect `docs/worktrees.md` and select an appropriate isolated source checkout.
This feature is not added to `experimental/PR_STACK.md` or marked ready for a composed build by this planning entry.

## Collector and GitHub workflow

Proposed flow: application crash -> private collector -> grouped crash -> review/threshold -> GitHub issue.

Create one issue per distinct crash group, including affected build IDs, frequency, a readable stack and a report link.
Sentry and BugSplat both document GitHub integrations; check the chosen subscription's actual capabilities.
Validate duplicate suppression and routing before enabling automatic creation.

A separate private issue repository can be used while application source remains local/private. Links from stack
frames to GitHub source require the corresponding source revision to exist there. Do not route experimental
SCADMaxx reports automatically into upstream OpenSCAD's tracker.

## Free plans and sponsorship research

Findings were checked in this chat on 2026-10-01; pricing and eligibility must be rechecked before signup.

| Service | Ordinary free plan | Open-source sponsorship |
| --- | --- | --- |
| Sentry | 5,000 errors/month. | Advertised 5 million errors, 10 GB attachments, Business features and no term limit; application required. |
| BugSplat | 15,000 crashes/month, 3 users, 100 GB storage and one-month retention. | Normally Team-equivalent: 25,000 crashes/month and 250 GB storage; tailored support for approved not-for-profit open-source projects. |

The Sentry sponsorship page listed the 5 million error allowance without an explicit period in the extracted text;
confirm the billing period and attachment/symbol limits with the actual plan. Sponsored quotas are not unlimited.

SCADMaxx's current private/local composition must be described accurately in any application. Eligibility is not
established merely by being based on OpenSCAD. Sentry requests project and license information; verify acceptance
of SCADMaxx's actual license and source availability. Do not publish anything solely to obtain sponsorship without
a separate user decision.

BugSplat's billing guide included GitHub in Free, while its current pricing page placed "Integrations & alerts"
under Team. Resolve this discrepancy before relying on the ordinary free tier for the complete GitHub workflow.
The proposed first choice is to investigate Sentry sponsorship; an ordinary free account can support a prototype.

## Indicative effort and validation

These are engineering estimates, not vendor promises or measured implementation results:

- First Windows capture demonstration: roughly half a day to one day.
- Dependable Windows integration including packaging, symbols, consent and validation: roughly 3-5 developer-days.
- Hosted project/collector configuration: roughly 1-3 hours once account access is available.
- Basic GitHub configuration and validation: a few hours.
- Proper self-hosted deployment: roughly 1-2 additional days, plus ongoing operations.

The initial demonstration should deliberately crash a freshly extracted distribution and show correct function
names/source lines and release identity in the collector. Subsequent checks should cover a worker-thread crash,
offline retry, disabled-upload behavior, writable storage under a normal user account, symbol matching across two
builds, and repeated reports mapping to a single GitHub issue. Keep deliberate crashes isolated from user work.

## Decisions still open

- Final provider and hosted versus self-hosted operation.
- Sponsorship eligibility, actual quotas and fallback if sponsorship is unavailable.
- Consent experience, report contents, retention, collector region and access permissions.
- GitHub destination, visibility, issue template and manual versus automatic creation policy.
- Windows-only first delivery and whether hang reporting or other platforms warrant later features.

No other unfinished feature is currently identified as a hard prerequisite; symbol handling belongs in this feature.

## References

- [Sentry Native SDK](https://github.com/getsentry/sentry-native)
- [Sentry open-source sponsorship](https://sentry.io/for/open-source/)
- [Sentry free and sponsored plan changes](https://sentry.zendesk.com/hc/en-us/articles/40116900282011-How-is-my-plan-changing-August-27-2025)
- [Sentry sponsored quota policy](https://sentry.zendesk.com/hc/en-us/articles/24544821258523-Can-I-increase-the-quota-on-my-sponsored-plan)
- [Sentry integration capabilities](https://docs.sentry.io/api/integrations/get-integration-provider-information/)
- [Sentry self-hosting requirements](https://github.com/getsentry/self-hosted/blob/master/install/_min-requirements.sh)
- [BugSplat platform support](https://www.bugsplat.com/platforms/)
- [BugSplat pricing](https://www.bugsplat.com/pricing/)
- [BugSplat open-source plan](https://docs.bugsplat.com/administration/billing/free-plans-from-bugsplat/bugsplat-free-accounts-for-not-for-profit-open-source-projects)
- [BugSplat billing guide](https://docs.bugsplat.com/administration/billing/plans-and-billing-guide)
- [BugSplat GitHub integration](https://docs.bugsplat.com/introduction/development/integrating-with-tools/issue-trackers/github-issues)
