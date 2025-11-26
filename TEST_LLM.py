import time
from src.llm_groq import GroqLLM

BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
CYAN = "\033[96m"


def print_header(text):
    print(f"\n{BOLD}{CYAN}{'='*80}\n{text}\n{'='*80}{RESET}")


def test_llm():
    print_header("🔍 Testing Groq LLM (Improved Mode)")

    print(f"{YELLOW}Initializing GroqLLM...{RESET}")
    t0 = time.time()
    llm = GroqLLM()
    t1 = time.time()

    if llm.connection_status:
        print(f"{GREEN}🟢 Connected successfully!{RESET}")
        print(f"{CYAN}Model: {llm.model}{RESET}")
        print(f"⏱ Initialization Time: {round(t1 - t0, 3)} sec")
    else:
        print(f"{RED}🔴 Connection FAILED!{RESET}")
        return
    
    print_header("🧪 Sending Sample Query")

    query = "Explain polymorphism in Java with example."

    t2 = time.time()
    response = llm.generate_answer(query, [], [])
    t3 = time.time()

    print(f"⏱ Response Time: {round(t3 - t2, 3)} sec")

    if response["status"] == "success":
        print(f"{GREEN}✅ LLM Response Received:{RESET}\n")
        print(response["answer"])
    else:
        print(f"{RED}❌ ERROR:{RESET} {response['answer']}")

    print_header("📊 Test Completed Successfully")


if __name__ == "__main__":
    print(f"{BOLD}{CYAN}🚀 Running Improved LLM Test Script{RESET}")
    test_llm()
