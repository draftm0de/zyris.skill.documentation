# Publish with approval

## Prepare

Ask the Manager to prepare publication for this repository. It reviews changes and destination, proposes a commit message, and prepares PR text, explicit files and checks. No commit, push or PR occurs before approval. A changelog can record dated changes but is not mandatory.

## Approve

Review the diff, message, repository, branch and merge method. An example request is: “May I commit these changes with the shown message, push to the specified branch, create the PR and merge after passing checks and required reviews?” This is an example, not a current approval request. Partial approval permits only the named steps.

## Execute and resume

The host performs Git/GitHub operations; the local helper only records the plan, approval and observed stages. Publish ends at the observed merge. No version selection, tags, releases or catalog promotion. Errors preserve the reached state; changed content needs fresh review and approval. Journals stay outside source and installation. Old release journals cannot resume in the new workflow.

## Limits

GitHub access and suitable host tools are needed. GitLab MRs are not integrated. Branch rules and required reviews remain binding. A merged plugin is available in the repository marketplace; existing users may need to sync. The full live publication workflow has not been separately accepted.

[Usage](usage.md) · [Installation](installation.md)
