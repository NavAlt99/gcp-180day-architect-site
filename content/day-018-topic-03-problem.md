**Failure:** A storage bucket seems to disappear after the learner changes tabs. They create a second bucket, then discover the first in another project. Two resources now exist and both may incur storage or request charges.

**Cause:** The project picker changed between screens. The learner treated the service navigation shortcut as though it preserved the previous project context.

**Fix:** Stop creating resources. Compare the project ID in the top bar with the intended lab project. Search the authorized projects for the first bucket, identify its owner and contents, then delete only the accidental resource after checking it has no needed data. Record the project ID and region before every creation step in future labs. Verify the resource list again and inspect Billing for unexpected usage.
