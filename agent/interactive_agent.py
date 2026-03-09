"""交互式Android Agent"""
from android_agent import run_agent

def main():
    print("=== Android Agent 交互模式 ===")
    print("输入任务，Agent会自动选择工具完成")
    print("输入 'quit' 或 'exit' 退出\n")

    while True:
        task = input("\n请输入任务: ").strip()

        if task.lower() in ['quit', 'exit', 'q']:
            print("退出Agent")
            break

        if not task:
            continue

        try:
            result = run_agent(task, max_steps=30)
            print(f"\n{'='*50}")
            print(f"任务完成: {result}")
            print(f"{'='*50}")
        except KeyboardInterrupt:
            print("\n\n任务被中断")
            break
        except Exception as e:
            print(f"\n错误: {e}")

if __name__ == "__main__":
    main()
