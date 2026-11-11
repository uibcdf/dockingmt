# Public GitHub Release titles

Follow the [canonical release-title rule](../MOLSYSSUITE_GUIDE.md#github-release-titles)
and [suite release policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md#github-release-titles).
The public component release title/name is exactly its canonical `X.Y.Z` version,
matching the tag and package/project version. Put descriptions in the body/notes.

Before publishing or intentionally editing a release, check **Release title**
in the web form, pass `--title X.Y.Z` to GitHub CLI, or set API `name` to the same
canonical value as `tag_name`. Generating release notes does not remove this check.
The existing governance policy-release/archive namespaces and documented bounded
exception route retain their separate meanings.

Accepted decision: [uibcdf/molsyssuite#119](https://github.com/uibcdf/molsyssuite/issues/119),
coordinated with [uibcdf/moli#68](https://github.com/uibcdf/moli/issues/68).

The [prospective release ladder](RELEASE_MILESTONES.md) distinguishes a source
tag, GitHub Release and actual Conda package. Publishing a GitHub Release currently
activates the Conda wrapper; review the route and exact candidate before that event.

## Availability announcement

Maintainer decision, 2026-10-23, tracked in
[BindingMT #47](https://github.com/uibcdf/bindingmt/issues/47): after both the new
public package and its matching GitHub Release are available, open an issue in
[`uibcdf/molsyssuite`](https://github.com/uibcdf/molsyssuite/issues) announcing the
available version, with links to the package and release. Record the announcement
link in the publication closeout. This is a post-publication action, not a release
decision or permission to publish an unqualified candidate.

The subsequently adopted [suite notice rule](../MOLSYSSUITE_GUIDE.md#release-and-package-publication-notices)
also requires a release-specific MolSysSuite issue for a source/tag-only component
release, even before a package exists. State the absent package explicitly and
update that same notice when artifacts arrive. The maintainer's request above
remains due when both the public package and matching Release are available;
waiting for the package does not suppress an earlier source-release notice.
No notice is due merely for a prospective roadmap version.
