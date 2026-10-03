# Supplied receive sequence
1. NIC receive queue
2. Driver processing / DMA / notification
3. NAPI polling
4. IP input and local delivery
5. Transport demultiplexing and socket buffer
6. Application reads bytes
Loopback bypasses physical NIC/DMA. Queued bytes do not prove application read.
