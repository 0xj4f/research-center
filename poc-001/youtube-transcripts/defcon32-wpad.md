# Exposing WPAD Vulnerabilities: A 25-Year-Old Security Issue

**Presenter:** Thomas

---

## Introduction

Hello, my name is Thomas. In my daily work, I focus on incident response and forensics. I've also done some red team engagements, and during those, I often use a tool called **Responder**, which has a function to set up a rogue proxy server using the **WPAD** (Web Proxy Auto-Discovery Protocol) function. By monitoring the network, I can see traffic where clients are asking for the WPAD domain within a company. Sometimes, they even ask for **wpad.tld** (top-level domain).

This made me wonder: Who owns these domains? Are they in use? Are they free? Can I buy them? What are they being used for?

---

## The Quest for WPAD Domains

At the time, I discovered that a German individual owned the Danish WPAD domain **wpad.dk**. I wasn't sure what he was using it for. Two years later, I checked again and found that someone in Israel had acquired the Danish domain. In 2020, the Danish registry for **.dk** domains added a function where you could sign up for a waiting list. I signed up and paid a small fee every year.

---

## How WPAD Works

### Basic Web Request Flow

- **Standard Process:**
  - A client requests a web page.
  - It queries the DNS server to find the IP address.
  - Connects to the web server.
  - Retrieves the content.

- **With a Proxy Server:**
  - The client asks the proxy server.
  - The proxy server resolves the domain name and retrieves the web page.
  - Returns the content to the client.

### Introduction of WPAD

Back in 1996, Netscape decided there needed to be an easier way to automatically configure machines when they join a network. They came up with the **WPAD** function to automatically locate the configuration file for proxy settings.

They set up a consortium to try to make it an RFC standard, but it never materialized, and it expired in 1999—making it a 25-year-old issue now.

---

## The Security Issue with WPAD

According to Wikipedia, the way WPAD works is:

1. The client, say **client.a.company.com**, will attempt to resolve **wpad** when the browser is opened.
2. It will remove the client name and try **wpad.a.company.com**.
3. If that doesn't work, it removes another level and tries **wpad.company.com**.
4. If still unresolved, it might eventually try **wpad.tld**, like **wpad.dk**.

In some implementations, it incorrectly goes down to **wpad.tld** and downloads the configuration file from there. This is a security issue because:

- An external entity owning **wpad.tld** can serve malicious configuration files.
- The client trusts and executes the downloaded JavaScript file on the local machine.
- This can lead to man-in-the-middle attacks, credential theft, and more.

---

## My Experiment with WPAD.dk

### Acquiring the Domain

In March 2023, I received an email from the Danish registry **DK Hostmaster** saying that the **wpad.dk** domain was now available, and I could register it. I decided to do so to see if there was any traffic at all.

I set up a cheap VPS and added the domain to a web server, intending to monitor the logs.

### Historical Ownership

Looking into who owned this domain in the past:

- In 2007, someone in Denmark had it.
- It was then sold to individuals in Belgium, Germany, and Israel.
- Now, I acquired it in 2023.

---

## The Initial Results

On the **first day** of assigning **wpad.dk** to my server:

- I received **more than 880,000 requests** for the **wpad.dat** file.
- I was surprised by the volume of traffic without doing anything other than setting up the domain.

---

## Setting Up for Data Collection

### Custom Server Setup

- I set up a VPS with:

  - DNS server: Became my own name server on the internet.
  - Registered with DNSSEC.
  - Web server on top of that.

- This allowed me to:

  - Add the domains I acquired.
  - Capture all the traffic and logs in the way I wanted.

### Crafting a Web Page

- Created a basic web page using Notepad.
- Included a disclaimer stating:

  - The page shouldn't be used.
  - It's for research purposes.

---

## Enhancing Data Collection

### Dynamic JavaScript Generation

When a client downloads the **wpad.dat** file:

- The client executes the JavaScript on the local machine.
- The client cannot see its public IP address.
- To capture the public IP, I:

  - Built the JavaScript dynamically on the server.
  - Embedded the client's public IP into the script.
  - Each client gets a dedicated script with their public IP.

### Data Leakage via DNS

- By constructing specific DNS queries within the script, I could leak:

  - Time zone.
  - Internal IP address.
  - External (public) IP address.

- Example:

  - Client wants to go to **defcon.org**.
  - The script builds a DNS name like:

    ```
    D[TimeZone]I[InternalIP]W[ExternalIP].p.wpad.dk
    ```

- All traffic is sent to my server over unencrypted HTTP (port 80).

---

## Observations from the Logs

### Acquiring More Domains

- Decided to buy additional **wpad** domains:

  - Some TLDs are protected and cannot be registered (e.g., **wpad.com**, **wpad.net**, **wpad.org**).
  - Acquired domains like **wpad.id**, **wpad.in**, **wpad.site**, **wpad.biz**, **wpad.press**, **wpad.porn**, **wpad.vegas**.

- Also rented **wpad.io** for a year.

### Traffic Analysis

- Over one year (April to April):

  - Received **1.1 billion DNS requests**.
  - Generated **200 GB** of text log files from the DNS server alone.
  - Example logs showed clients requesting domains like **cnn.com**, revealing internal and public IP addresses.

---

## Geographic Distribution of Requests

- **wpad.dk**:

  - Expected high traffic from Denmark.
  - Surprisingly high traffic from Russia and Ukraine.
  - Significant traffic from Germany.

- **wpad.vegas**:

  - High traffic from the United States.
  - Mixed traffic from other countries.

---

## Impact on Client Machines

- When Windows machines connect to a network and cannot access the internet properly, they show a warning icon.
- Because my proxy server doesn't return any content, clients think they have no internet access.
- To fix this, I:

  - Identified six Microsoft domains that Windows checks to determine internet connectivity.
  - Configured my server to respond with "OK" for these domains.
  - Clients then indicated they had internet access again.

---

## Types of Requests Observed

### HTTP Methods

- **GET requests**: The majority.
- **POST requests**: Clients sending data to servers (37 million requests).
- **CONNECT requests**: Proxy traffic (1.1 billion requests).

### Services and Applications

- Clients tried to access various services through my proxy:

  - **Windows Update**.
  - **Antivirus updates**.
  - **VPN clients**.
  - **Microsoft SCCM client**.
  - **RealPlayer** updates.
  - And many more.

---

## Sensitive Data Exposure

### Internal Network Traffic

- Clients were sending internal network requests to my external proxy:

  - Example: A client at **192.168.1.5** trying to communicate with **192.168.1.1** via my proxy.
  - This should never happen, as internal traffic isn't resolvable on the internet.

### Credentials in URLs

- Found over **200,000 URL requests** containing usernames and passwords.
- Examples of weak credentials:

  - **admin:admin**
  - **change_me:change_me**
  - **security:party**

### Authentication Protocols

- Many clients were using outdated protocols like **NTLMv1**, which is insecure.
- Captured numerous authentication attempts with usernames and hashed passwords.

---

## Miscellaneous Observations

### User-Agent Strings

- Collected **27,000 different User-Agent strings**.
- Included clients from all platforms:

  - Windows
  - Linux
  - macOS
  - iOS
  - Android

### Potential Malicious Activity

- Detected scripts that seemed to monitor or manipulate traffic:

  - Some scripts were redirecting ad traffic, possibly to replace ad IDs and earn revenue.
  - Others were collecting data from failed domain resolutions.

---

## Interactions with Security Solutions

### Palo Alto Networks

- Noticed only one instance of detection:

  - Palo Alto's setup monitors URLs and categorizes them.
  - It replayed requests with a specific User-Agent string indicating it's a monitoring device.

### Cisco Endpoint Client

- Cisco's endpoint client is designed to protect against rogue DNS and proxy servers.
- However, because I returned error pages, the client became aggressive:

  - It started brute-forcing requests to my server.
  - I had to blackhole **opendns.com** to stop the DDoS-like behavior.

---

## User Feedback and Responses

- Included a feedback form on the error pages.

### Whitelisting Requests

- Received 40 requests from users wanting to be whitelisted.
- They provided computer names, which looked like internal hostnames.

### Survey Results

- Set up a survey asking users how they liked my non-working proxy.
- Surprisingly, the few responses leaned towards liking the service.

### Feedback Messages

- Some users were frustrated:

  - Complained about error messages when accessing banking sites or clicking email links.
  - Others offered to help optimize my website for SEO.

---

## Reflection and Conclusions

### Lack of Detection

- For one year, I monitored if anyone was discussing these domains or the issue.
- Found no discussions or indications of detection.

### The Big Question

- **Why can someone like me even buy these domains?**
- **Why hasn't this 25-year-old security flaw been addressed?**
- It's not a modern security model to download and execute a proxy script from an untrusted source.

---

## Recommendations

### Mitigation Steps

- **Add WPAD domains to the hosts file**, pointing them to **127.0.0.1** to prevent external resolution.
- **Disable WPAD at the system level**:

  - Disabling it only in the browser isn't sufficient.
  - System-level services (like antivirus software) may still use WPAD settings.

- **Windows Specifics**:

  - There's a Windows service called **WinHTTP Web Proxy Auto-Discovery Service**.
  - It can be challenging to disable due to dependencies.

- **Consult Documentation**:

  - Since the issue affects multiple platforms and applications, refer to official documentation for proper mitigation steps.

---

## Final Thoughts

- I don't know if in 25 years I'll be here again talking about the same issue.
- This 25-year anniversary highlights that nothing has changed regarding WPAD vulnerabilities.
- It's essential for organizations and developers to address this long-standing security issue.

---

## Acknowledgments

- **Special thanks to my friend Kiel Norman** for help with research and information.

---

## Bonus Information

### Contact from Another Researcher

- After my talk was scheduled for DEF CON, I was contacted by a researcher named Tom.
- He had been conducting similar research on other domain names.
- We considered sharing data, which could be insightful.

### Interaction with a Large Company

- After two months, I was contacted by a large company in Denmark.
- They noticed that many of their machines were querying my **wpad.dat** file.
- They reached out because one of my domains wasn't fully anonymized, and they traced it back to me.

---

## Conclusion

- The issue with WPAD is widespread, affecting all platforms and applications.
- It's not just a "Microsoft problem."
- The best course of action is to disable WPAD entirely and ensure that systems are not vulnerable to such attacks.

---

**Thank you for your attention.**

[Applause]