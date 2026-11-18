# Publish a plugin

## Requirements

Provide an accessible plugin repository, authenticated GitHub tools in the host and a resolved catalog destination. Local paths must actually be available in a cloud session. GitLab publication is not integrated yet.

## Request a proposal

In Claude: `/zyris-skill-manager:publish PATH`. In Codex: “Use ZYRIS Skill Manager to prepare publication of this plugin.”

The Manager reviews changes, proposes a version, prepares CHANGELOG.md, the commit message and PR text, validates packages/documentation, then shows the files and destinations. No commits, pushes, PRs or releases occur during preparation.

## Approve the whole proposal

For example:

> Proposed version: 0.2.0. Commit: “feat: add example capability”.
> Shall I commit and push these changes, create the PR, merge after successful checks, then publish the tag, release and specified catalog?

This is a fictional example, not a current publication request. Request changes to the version/messages or decline. Only explicit approval covering the entire listed workflow allows publication. Approval of a commit alone does not imply approval of merge/release.

## After approval

The Manager executes the steps, waits for checks/reviews and reports progress. Repository protections remain in force. No manual tag or release Action is needed; ordinary validation CI can continue.

## Stop and resume

You can stop at any time. Completed public actions are not automatically undone. A private journal outside the installation and source repositories records progress. Supply that journal and the original request when resuming; the Manager verifies actual remote state first. Changed content needs renewed approval. No unattended background publication.

## Limits

The host performs Git/GitHub operations; the journal helper itself does not publish or authenticate human consent. No live publication was performed during implementation. Missing catalog repositories are not created implicitly. A released version whose catalog promotion failed is reported as partial completion.

[Release operations](release-operations.md) · [Evidence](release-evidence.md) · [Usage](usage.md)
