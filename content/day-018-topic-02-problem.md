**Failure:** A learner deploys a supposedly free VM but selects a noneligible machine size and adds a disk and outbound traffic. Charges appear despite the product having a Free Tier entry.

**Cause:** The learner checked the product name only. The tier applied to a specific configuration and quantity, while attached resources and egress had their own pricing. An alerts-only budget notified the owner after cost accumulated; it did not stop usage.

**Fix:** Stop the workload and inventory every resource it created. Compare the selected region, machine, disk, network and expected monthly use with the current Free Tier terms and pricing. Delete unneeded resources, verify deletion and review Billing again. For future labs, record a cost estimate, an owner and an exit plan before provisioning. Treat an alerts-only budget as monitoring, not a universal spending cap.
