node_trust_scores = {}

# Register new node (only if it has a trust score)
def register_node(ip):
    if ip not in node_trust_scores:
        node_trust_scores[ip] = 50  # Start with neutral trust

# Report node behavior
def report_node(ip, successful_delivery):
    if successful_delivery:
        node_trust_scores[ip] += 10
    else:
        node_trust_scores[ip] -= 30
        if node_trust_scores[ip] < 0:
            del node_trust_scores[ip]  # Remove untrusted node
