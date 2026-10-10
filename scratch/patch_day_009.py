#!/usr/bin/env python3
import re
import urllib.parse

with open("scratch/day_data_009.py", "r", encoding="utf-8") as f:
    code = f.read()

sub2 = """<p><strong class="side-heading">Core hardware virtualization architectural mechanisms:</strong></p>
<ul>
<li><strong class="keyword">Intel VT-x / AMD-V (CPU Virtualization)</strong>: Adds specialized CPU modes—such as Intel VMX Root and Non-Root modes or AMD SVM (Secure Virtual Machine)—allowing guest operating systems to execute privileged instructions directly on the physical processor.</li>
<li><strong class="keyword">EPT / RVI (Memory Virtualization)</strong>: Intel Extended Page Tables (EPT) and AMD Rapid Virtualization Indexing (RVI, or Nested Page Tables) handle two-stage memory address translation directly in hardware. This eliminates the heavy overhead of maintaining software shadow page tables.</li>
<li><strong class="keyword">vCPUs (Virtual CPUs)</strong>: Logical processing units assigned by the hypervisor to a virtual machine, scheduled directly onto physical CPU cores via hardware virtualization extensions.</li>
<li><strong class="keyword">IOMMU (Intel VT-d / AMD-Vi)</strong>: Hardware-level Input/Output Memory Management Units that allow virtual machines to directly access physical hardware like GPUs and network cards (device passthrough).</li>
</ul>

<p><strong class="side-heading">How hardware-assisted virtualization operates:</strong></p>
<ul>
<li><strong class="keyword">Privilege Separation</strong>: The hypervisor runs in a high-privilege root mode, while the guest operating system runs in non-root mode.</li>
<li><strong class="keyword">VM Exits and Entries</strong>: When a guest OS attempts a sensitive hardware-level action, a VM exit safely transfers control to the hypervisor, which processes the request and hands control back via a VM entry.</li>
<li><strong class="keyword">Performance Gain</strong>: Older methods relied on slow software instruction interception or kernel modification (paravirtualization). Hardware extensions execute code directly, making multi-tenant cloud servers and local hypervisors like VMware Workstation or KVM practical.</li>
</ul>"""

sub3 = """<p><strong class="side-heading">The Linux KVM Subsystem (Kernel Space):</strong></p>
<ul>
<li><strong class="keyword">Hypervisor Role</strong>: KVM converts the Linux kernel into a Type-1 (bare-metal) hypervisor by loading kernel modules (<kbd>kvm.ko</kbd>, plus hardware-specific modules like <kbd>kvm-intel.ko</kbd> or <kbd>kvm-amd.ko</kbd>).</li>
<li><strong class="keyword">Hardware Acceleration</strong>: It leverages hardware virtualization extensions (such as Intel VT-x or AMD-V) to run guest CPU instructions directly on the physical processor at near-native speed.</li>
<li><strong class="keyword">Process Representation</strong>: Each virtual machine runs as a standard Linux process managed by the kernel scheduler and memory manager.</li>
<li><strong class="keyword">The /dev/kvm Interface</strong>: Userspace programs interact with KVM via the <kbd>/dev/kvm</kbd> character device node using ioctl system calls to create VMs, allocate guest memory, and inject interrupts.</li>
</ul>

<p><strong class="side-heading">The QEMU Userspace Model:</strong></p>
<ul>
<li><strong class="keyword">Device Emulation</strong>: KVM alone only handles CPU and memory virtualization; it relies on QEMU in userspace to emulate complete system hardware—including disk controllers, network cards, graphic adapters, and BIOS/UEFI firmware.</li>
<li><strong class="keyword">VM Exits and Hand-offs</strong>: When a guest operating system tries to access a virtualized device or trigger a privileged event that KVM cannot handle directly, a VM exit occurs. Execution transfers from KVM to the QEMU userspace process to handle the device emulation in software before returning control back to the guest.</li>
<li><strong class="keyword">Paravirtualization (Virtio)</strong>: To bypass slow device emulation overhead for high-throughput disk and network I/O, QEMU and KVM utilize virtio paravirtualized drivers, allowing the guest and host to communicate efficiently through shared memory rings.</li>
<li><strong class="keyword">Management &amp; Control</strong>: QEMU acts as the Virtual Machine Monitor (VMM), often orchestrated via higher-level management APIs and tools like <kbd>libvirt</kbd> and <kbd>virt-manager</kbd>.</li>
</ul>"""

sub4 = """<p><strong class="side-heading">Compute Engine Hypervisor Architecture:</strong></p>
<ul>
<li><strong class="keyword">Direct Hardware Access</strong>: The hypervisor operates as a bare-metal abstraction layer, scheduling vCPUs and managing physical memory without a general-purpose host operating system in the data path.</li>
<li><strong class="keyword">Verified Boot Stack</strong>: Physical servers execute a cryptographically verified boot chain where every layer—from the physical host firmware up to the hypervisor—must pass digital signature validation before loading.</li>
<li><strong class="keyword">Tenant Isolation</strong>: Hardware-assisted virtualization extensions (Intel VT-x / AMD-V) and memory management unit (IOMMU) controls isolate guest memory spaces and network traffic per project and instance.</li>
</ul>

<p><strong class="side-heading">Shielded VM Security Components:</strong></p>
<p>Google Cloud Shielded VMs extend protection from the hypervisor layer into the guest operating system using three primary capabilities:</p>
<ul>
<li><strong class="keyword">Secure Boot</strong>: Uses Unified Extensible Firmware Interface (UEFI) firmware to verify the digital signatures of all early-boot components, kernels, and kernel modules before they execute, blocking unsigned bootloaders or rootkits. (Enabled via explicit opt-in due to compatibility requirements like ARM64 or out-of-tree drivers).</li>
<li><strong class="keyword">Virtual Trusted Platform Module (vTPM)</strong>: Provides a hardware-grade, virtualized TPM 2.0 chip dedicated to the instance. It performs Measured Boot by recording cryptographic hashes of boot components into Platform Configuration Registers (PCRs) and securely stores encryption keys. (Enabled by default).</li>
<li><strong class="keyword">Integrity Monitoring</strong>: Continuously tracks boot measurements against a baseline policy through Cloud Monitoring/Operations suites to flag unexpected kernel or boot modifications. (Enabled by default alongside the vTPM).</li>
</ul>"""

post_script = r'''

# --- POST-PROCESSING ENHANCEMENTS FOR DAY 9 ---
import re, urllib.parse

_t0 = DATA['topics'][0]
_t0['technical'] = _t0['technical'].replace(
    '<h4>The Linux KVM Subsystem and QEMU Userspace Model</h4>',
    ''' + repr(sub2) + r''' + '\n\n<h4>The Linux KVM Subsystem and QEMU Userspace Model</h4>',
    1
)
_t0['technical'] = _t0['technical'].replace(
    '<h4>Compute Engine Hypervisor Architecture and Shielded VM Security</h4>',
    ''' + repr(sub3) + r''' + '\n\n<h4>Compute Engine Hypervisor Architecture and Shielded VM Security</h4>',
    1
)
_t0['technical'] = _t0['technical'].replace(
    '<h4>Guest Kernel Autonomy vs Hypervisor Management Overhead</h4>',
    ''' + repr(sub4) + r''' + '\n\n<h4>Guest Kernel Autonomy vs Hypervisor Management Overhead</h4>',
    1
)

def _link_keywords(html_text):
    def _repl(m):
        inner = m.group(1)
        if '<a ' in inner:
            return m.group(0)
        clean_text = re.sub(r'<[^>]+>', '', inner).strip()
        search_url = 'http://www.google.com/search?q=' + urllib.parse.quote_plus(clean_text)
        return '<strong class="keyword"><a href="' + search_url + '" target="_blank" rel="noopener">' + inner + '</a></strong>'
    return re.sub(r'<strong class="keyword">(.*?)</strong>', _repl, html_text)

for _topic in DATA['topics']:
    _topic['technical'] = _link_keywords(_topic['technical'])

for _topic in DATA['topics']:
    _technical = _topic['technical']
    _headings = re.findall(r'<h4>(.*?)</h4>', _technical, re.S)
    _links = []
    for _number, _heading in enumerate(_headings, 1):
        _anchor = f"{_topic['key']}-subtopic-{_number:02d}"
        _technical = _technical.replace(
            '<h4>' + _heading + '</h4>',
            f'<h4 id="{_anchor}">' + _heading + '</h4>', 1
        )
        _links.append(f'<li><a href="#{_anchor}">{_heading}</a></li>')
    _linked_list = '<ul>' + ''.join(_links) + '</ul>'
    _technical = re.sub(
        r'(<p><strong class="side-heading">Subtopics in this discussion:</strong></p>)\s*<ol>.*?</ol>',
        lambda match: match.group(1) + _linked_list,
        _technical, count=1, flags=re.S
    )
    _topic['technical'] = _technical
    _topic_key = _topic['key']
    _nav_links = f'<p><a href="#{_topic_key}-technical">Technical discussion →</a> <a href="#{_topic_key}-problem">Real-world problem →</a> <a href="#{_topic_key}-lab">Step-by-step lab →</a></p>'
    _card_pat = r'(<article class="topic-card overview" id="' + _topic_key + r'-overview">.*?)(</article>)'
    DATA['part1_html'] = re.sub(
        _card_pat,
        lambda m: m.group(1) + '<p><strong class="side-heading">Linked subtopics:</strong></p>' + _linked_list + '\n' + _nav_links + '\n' + m.group(2),
        DATA['part1_html'], count=1, flags=re.S
    )
'''

with open("scratch/day_data_009.py", "w", encoding="utf-8") as f:
    f.write(code + post_script)
print("Updated scratch/day_data_009.py successfully.")
