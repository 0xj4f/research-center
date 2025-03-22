# Grand Theft Actions: Abusing Self-Hosted GitHub Runners at Scale

**Presenters:**
- **Adnan Khan**
- **John Stawinsky**

---

## Introduction

Hello everyone! Let's address the burning question in the room: **No, we did not get access to the source code for Grand Theft Auto 6, nor do we know if the game will ever be released.** Maybe in a future presentation, but not today.

This is **"Grand Theft Actions: Abusing Self-Hosted GitHub Runners at Scale."**

Before we get started, we read online that as long as we have a disclaimer, nobody's allowed to sue us. So here we go:

**Disclaimer:** All vulnerabilities mentioned during this talk have been remediated. The views and opinions expressed are solely our own, and the content is not endorsed by nor does it represent the views of our employers.

---

## About Us

### Adnan Khan

- **Profession:** Security Engineer
- **Roles:**
  - Security Researcher
  - Bug Bounty Hunter
- **Socials:** [Not Provided]

### John Stawinsky

- **Profession:** Red Team Security Engineer
- **Roles:**
  - CICD Security Researcher
- **Fun Facts:**
  - Watched *Avatar: The Last Airbender* three times (animated version)
  - Former collegiate wrestler

---

## Understanding GitHub Runners

We're going to be talking a lot about self-hosted runners today, so let's ensure everyone has a background understanding of how GitHub runners work.

### GitHub-Hosted Runners

- Built by GitHub and updated frequently.
- Cover a wide variety of operating systems and architectures.
- **Ephemeral:** Torn down at the conclusion of each workflow job.

### Self-Hosted Runners

- Managed and secured entirely by the end user.
- Often configured in a less secure manner due to the path of least resistance.
- Both GitHub-hosted and self-hosted runners serve GitHub Actions workflows triggered from repositories on GitHub.

---

## Why Are We Here Today?

All the organizations and projects you see on the screen have used self-hosted runners on their public GitHub repositories. Not only that, but they used them in an insecure manner. Over the last 12 months, we were able to identify vulnerabilities in these organizations and many more that we can't talk about. Some of these cases could have led to widespread critical supply chain attacks.

You may be wondering if we just showed that last slide to flex our cool vulnerabilities at DEF CON. I just want to go on record saying that, **yeah, pretty much.** But it also raises a bigger question: **Why were we in a position to execute supply chain attacks on all of these companies?**

The reason is that **GitHub Actions provides a broad attack surface** that exposes these organizations to compromise, especially when they use self-hosted runners.

---

## How We Got Started

Our vulnerability research campaign began back in **August 2022** when I was working on a red team with my former employer. I was fairly new to red teaming at the time and tripped a canary, getting kicked out of the client's network. While trying to get back in, we did some social engineering and found that we could use a GitHub access token we obtained to execute a workflow and persist on a non-ephemeral self-hosted runner inside that client's network. That got us back in, and we reached our objective.

That led to a talk at **ShmooCon** called **"Phantom of the Pipeline"** given in January 2023 and the release of the original **gato** tool. Around the time that Adnan, Mason Davis, and Mossy were developing gato, I joined them on the red team, and gato was my entry to CICD security.

We started using gato to identify GitHub Actions vulnerabilities during red team engagements and then dove deeper into GitHub Actions abuse, especially around post-exploitation. As we were doing our research, we brainstormed ways to expand this from internal red team engagements to everybody, and Adnan had an idea that really took it to the next level.

---

## Expanding Our Research

One of the little asterisks at the end of the ShmooCon presentation was that if you fixed a typo on a public repository that was using a non-ephemeral self-hosted runner, you could make a pull request and modify the workflow file to get persistence. I demonstrated that vulnerability against the **GitHub Actions Runner Images** repository, which was accepted as a critical vulnerability.

After hacking GitHub Actions Runner Images, we started looking at all public repositories and realized that these misconfigurations were everywhere. We decided to team up. Our first joint operation was breaching Microsoft's perimeter by getting code execution on a domain-joined machine through **Microsoft DeepSpeed**, and then we launched a series of attacks, the next one of which we will cover today.

---

## Discovering Vulnerabilities at Scale

At a high level, there are three steps to discovering this vulnerability at scale:

1. **Search for Candidate Repositories:**
   - Use a combination of GitHub code search and Sourcegraph code search dorks.
   - Both have pros and cons, so we used both and deduplicated the results to get a list of candidate repositories.

2. **Analyze for Non-Ephemeral Runners:**
   - Use the tool **gatoX** to automate workflow run log analysis to determine if there's a non-ephemeral self-hosted runner in use.

3. **Plan the Attack:**
   - Determine if you can exploit the repository and achieve significant impact.

Self-hosted runner takeover is a special case of **public poison pipeline execution**. Anytime you can get your own code executed by a GitHub Actions workflow, you can conduct a poison pipeline attack. In the case of self-hosted runners, we'll use this to deploy persistence on the self-hosted runner via pull request, opening up lateral movement and privilege escalation paths.

---

## The Problem with Insecure Defaults

Misconfigurations are amplified by insecure defaults. The default setting for pull request approval on the pull request trigger is that it only requires approval for **first-time contributors**. If someone has a pull request—no matter how trivial—merged into the default branch, they won't need approval for workflow executions on their pull requests. **This is a bad, insecure default.**

---

## Case Study: Playing with Fire (PyTorch Attack)

### What is PyTorch?

- A machine learning framework originally developed by Meta.
- Open-sourced and used by companies around the world like Google, Lockheed Martin, OpenAI, and more.
- Backdooring PyTorch could allow compromising developers and organizations in the AI/ML space.

### Initial Reconnaissance

The hardest part of compromising PyTorch was searching through their workflows:

- Over **90 workflows**.
- Over **15 GitHub secrets**.
- More than **five self-hosted runners**.
- I manually mapped out the data flow through all of these workflows, many of which were nested, in preparation for this attack.

### Identifying Self-Hosted Runners

When we confirm that a repository has a self-hosted runner, we look at the workflow logs:

- The workflow shows the runner name, runner group name, and machine name.
- We saw that this is a **Jenkins runner**—a self-hosted runner attached to their public repository in the default group.
- This is one of the runners that we ended up compromising.

### Exploiting Default Settings

For busy repositories like PyTorch, you can often determine that the default approval requirements are in place:

- Look for a pull request submitted by a previous contributor that's from a fork.
- Check that the workflow run associated with it was not approved and that it ran on the pull request trigger.
- When these conditions are met, it's likely that the default approval requirements are in place.

GitHub warns against attaching self-hosted runners to public repositories, but the documentation and warnings are not obvious. Developers may not come across this documentation when registering a self-hosted runner.

---

## Infiltrating the Contributor List

To take advantage of those default approval settings, we needed to infiltrate the contributor list:

- We became the **grammar police**.
- Ran their markdown files through Grammarly, fixing typos and grammatical errors.
- Even trivial changes can make you a contributor once merged.
- We noticed "resolved" was in the past tense and should have been in the present tense.
- Fixed it and submitted a pull request.
- A few days later, it got merged, and we were officially contributors.

---

## Installing Command and Control

### Phase Two: Runner-on-Runner

This is where the hacking starts:

- **Runner-on-Runner:** Install another self-hosted runner on their self-hosted runner.
- Benefits:
  - All traffic goes to the same domains and IP addresses as the original runner.
  - Likely to fly under the radar of any EDR monitoring software.

### Exploiting the Default

- Modified the workflow in our fork to install our C2.
- The second runner is attached to our private C2 repository.
- We can task it to execute commands—essentially a web shell.
- Using this web shell, we're able to look around the file system and learn about the host, preparing for phase three.

---

## The Great Secret Heist

### Phase Three: Post-Exploitation

- **Self-hosted runner post-exploitation** is how you go from trivial RCE to a complete supply chain attack.
- Organizations didn't realize the actual impact unless we demonstrated it.

### The Magical GitHub Token

- Used by all GitHub Actions workflows to authenticate to GitHub for API or Git operations.
- An OAuth bearer token with multiple scopes (read or write).
- Configured at the repository or organization level or specified within each specific workflow file.
- Tokens are only valid for the duration of each job within a workflow.

### Privilege Escalation

- The GitHub token in PyTorch workflows had all the right permissions.
- The runner is the same one that we now have C2 on.
- When a workflow uses the `actions/checkout` step, the GitHub token is stored on the self-hosted runner file system.
- GitHub tokens from fork PRs only have read permissions.
- Solution: Persist on the runner and capture a token from a future workflow.

---

## Executing the Attack

### The Setup

- **Workflow from Fork PR:**
  - No access to secrets.
  - GitHub token with only read permissions.
- **Workflow from Base Repository:**
  - Has access to secrets.
  - GitHub token with write permissions.
- **Both execute on the same self-hosted runner.**

### Compromising the GitHub Token

- We waited for a future workflow from the base repo to execute on the runner.
- Captured the GitHub token from the `git config` file at runtime.
- Compromised that GitHub token, which we could use for the duration of the build.

### Deleting Workflow Run Logs

- We deleted the workflow run logs to avoid getting caught.
- Important for demonstrating impact to Meta's triage team.

---

## Tampering with GitHub Releases

- Used the compromised GitHub token to modify GitHub releases.
- Changed the release name to include our name.
- Sent a `curl` request using the GitHub API.
- Took a screenshot and then reverted it immediately.

---

## Exfiltrating GitHub Secrets

### The Crown Jewels

- GitHub secrets are the crown jewels of any repo that uses GitHub Actions.
- Often overprivileged and can provide lateral movement opportunities beyond the GitHub repository.
- PyTorch was using personal access tokens, AWS keys, and more.

### Recap of Our Actions

1. Fixed a typo and became contributors.
2. Installed our C2 on their self-hosted runners.
3. Stole a GitHub token from a future build.
4. Modified the release title.
5. Created a feature branch and injected code.
6. Stole GitHub personal access tokens and AWS keys.
7. Demonstrated various paths for supply chain compromise.

### AWS Key Compromise

- Repeated the process to grab their AWS keys.
- Used the AWS CLI to authenticate as the PyTorch bot user.
- Found PyTorch releases in the S3 buckets.
- Realized that users installing PyTorch via pip were downloading releases from these S3 buckets.
- With those AWS keys, we could have uploaded our own PyTorch releases, leading to a widespread supply chain attack.

---

## Disclosure Timeline

You would think that this amount of demonstration of impact would be enough to convince PyTorch to immediately apply fixes.

- **August 2023:** Submitted the issue to Meta Bug Bounty.
- **One Month Later:** Meta said there's no update to provide.
- **Two Months Later:** Meta said they consider the issue mitigated.
- We tested and found that anyone could still compromise their runners.
- Sent proof that the issue was not fully mitigated.
- **Another Two Months Later:** Meta applied some other fixes.
- Met with two of the PyTorch maintainers who were very concerned about these issues.
- It worried us that PyTorch was potentially vulnerable for this long.

---

## Introducing "gatoX"

This attack took a lot of hands-on keyboard workflow modification, so we wanted to automate it.

- **gatoX:** A tool we've open-sourced this week that automates the self-hosted runner takeover process.
- Now, instead of all that work, you fix a typo, become a contributor, then run gatoX.
- One of two things happens:
  - You get a shell and you're on top of the world.
  - You learn that approval is required, and you're sad because you didn't get to hack anything.

### Demo of "gatoX"

1. Enumerate a runner to confirm it's non-ephemeral.
2. Fix a typo and create a pull request.
3. Merge the typo fix PR.
4. Delete the fork to prepare for gatoX.
5. Run gatoX with the appropriate configuration.
6. gatoX creates a draft pull request deploying the runner-on-runner payload.
7. Wait for the runner to connect to GitHub and check back into the repository.
8. Drop into a shell and execute commands.

### Hall of Fame

- Finding CICD misconfigurations in open-source repositories can be a thankless job.
- We've added a Hall of Fame on the gatoX wiki.
- If you use gatoX to find a pull request injection or self-hosted runner vulnerability and the maintainers fix it, we'll add your name to the wiki.

---

## Additional Tactics and Techniques

We showed the technical TTPs we used during our PyTorch attack, but there are a bunch of other tactics we've used on other targets.

### SolarWinds-Style Build Compromise

- After getting persistence on a runner, modify scripts for the build or source code after it's checked out.
- The final build artifacts are poisoned without being linked back to the original source code—a stealthy supply chain attack.

### GitHub Release Asset Tampering

- If you have a contents write token, use the API to delete the old asset and upload a new one.
- The only indicator of compromise is the timestamp when a user looks at it through the web interface.

### Post-Checkout Hook

- Place a script into the `git hooks` directory of the repository on the compromised runner.
- The script exfiltrates data and sleeps, extending the build time without breaking the workflow.

---

## Defending Against These Attacks

### GitHub's Role

In our opinion, GitHub can:

- **Increase Warnings and Awareness:**
  - Make warnings more obvious when attaching self-hosted runners to public repos.
- **Improve Secure Defaults:**
  - Change insecure default settings, such as pull request approvals.
- **Implement Granular Approval Requirements:**
  - Provide more options to balance security and developer workflow efficiency.

### Organizational Defenses

Start with the easy steps:

- **Require Approval for All Outside Collaborators:**
  - Change the settings to enhance security.
- **Set the GitHub Token to Read-Only:**
  - Prevent post-exploitation opportunities.
- **Use Fine-Grained Personal Access Tokens:**
  - Limit the scope and reduce risks associated with compromised tokens.

### Securing Self-Hosted Runners

- **Make Runners Ephemeral:**
  - Use tools like GitHub's Actions Runner Controller or cloud provider autoscaling groups.
- **Consider Third-Party Solutions:**
  - Use turnkey drop-in replacements for GitHub runners that are ephemeral.
- **Implement Runner Group Pinning:**
  - Restrict which workflows can use the runner, protecting your most privileged runners.

---

## Conclusion

This talk and this research are not about PyTorch specifically. We've been able to do similar attacks on many advanced, mature organizations due to a lack of awareness around CICD agent security.

- We've submitted over **20 high and critical bug bounty submissions**, including critical vulnerabilities in GitHub Actions, Microsoft, PyTorch, TensorFlow, and more.
- Internally, CICD security is often a nightmare, becoming the new Active Directory Certificate Services (ADCS) for attackers.
- The main issue we see is a lack of awareness.

**We urge everyone to learn about these attacks to protect your organization from compromise.** If developers, architects, executives, and others are aware of these attacks, they'll be better equipped to implement controls that protect against the next critical supply chain attack.

**The moral of the story is: Learn about this stuff and don't let this be you.**

---

## Acknowledgments

We want to thank all of the bug bounty triage teams that handled some of the reports and applied solid mitigations to their products.

Thank you to everyone who showed up today and helped us raise awareness.

We'd like to thank DEF CON for giving us this platform. We've wanted to speak here for a long time, so this has been really fun.

Please, we don't have time for questions, but come find us after if you want to talk more.

**Thank you, everybody!**