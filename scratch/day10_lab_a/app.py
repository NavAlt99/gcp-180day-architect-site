import os, sys, time

def write_unbuffered_record(path, record_id):
    with open(path, "a") as f:
        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:BUFFERED\n")

def write_durable_record(path, record_id):
    with open(path, "a") as f:
        f.write(f"ORDER_RECORD:{record_id}:{time.time()}:DURABLE\n")
        f.flush()
        os.fsync(f.fileno())

if __name__ == "__main__":
    mode = sys.argv[1]
    target_dir = sys.argv[2]
    out_file = os.path.join(target_dir, "orders.log")
    if mode == "ephemeral":
        write_unbuffered_record(out_file, "ORD-9001")
    elif mode == "durable":
        write_durable_record(out_file, "ORD-9002")
