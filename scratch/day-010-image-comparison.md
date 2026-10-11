# Day 10 image optimization report

| Image | Image bytes | Archive bytes | FS layers | Inode proxy |
|---|---:|---:|---:|---:|
| single | 347506381 | 347275264 | 9 | 19220 |
| multi | 5775390 | 5773312 | 1 | 1 |
| delete | 347508648 | 346200064 | 10 | 19168 |

Logical uncompressed image size and saved archive bytes; not registry compressed transfer, shared cache disk usage or a CVE scan.
Rootfs inode proxy excludes duplicate hard-link entries; overlay host inodes and shared layers are runtime dependent.
Single stage inherits SDK and build cache; final scratch stage inherits only the copied static binary.
No GCP deployment or GKE performance measurement was performed.
