import tkinter as tk
from tkinter import messagebox
import subprocess
from prettytable import PrettyTable

# 日志输出函数
def log_message(message):
    log_display.config(state="normal")
    log_display.insert(tk.END, message + "\n")
    log_display.config(state="disabled")
    log_display.see(tk.END)

def create_conda_env():
    env_name = env_name_entry.get()
    env_path = env_path_entry.get()
    python_version = python_version_entry.get()
    packages = packages_entry.get().split()

    if not env_name:
        messagebox.showerror("错误", "环境名称不能为空！")
        return

    # 构造命令
    command = ["conda", "create"]
    if env_path:
        command.extend(["--prefix", env_path])
    else:
        command.extend(["-n", env_name])
    if python_version:
        command.extend(["python=" + python_version])
    if packages:
        command.extend(packages)
    command.append("-y")  # 自动确认创建环境

    # 执行命令
    try:
        log_message("正在创建环境...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        log_message(result.stdout)
        if env_path:
            messagebox.showinfo("成功", f"环境 {env_name} 在路径 {env_path} 创建成功！")
        else:
            messagebox.showinfo("成功", f"环境 {env_name} 创建成功！")
    except subprocess.CalledProcessError as e:
        log_message(f"创建环境时出错：{e.stderr}")
        messagebox.showerror("错误", f"创建环境时出错：{e.stderr}")

def delete_conda_env():
    env_name = delete_env_name_entry.get()
    env_path = delete_env_path_entry.get()

    if not env_name and not env_path:
        messagebox.showerror("错误", "环境名称或路径不能为空！")
        return

    # 构造命令
    command = ["conda", "env", "remove"]
    if env_path:
        command.extend(["--prefix", env_path])
    else:
        command.extend(["-n", env_name])
    command.append("-y")  # 自动确认删除环境

    # 执行命令
    try:
        log_message("正在删除环境...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        log_message(result.stdout)
        if env_path:
            messagebox.showinfo("成功", f"环境在路径 {env_path} 已成功删除！")
        else:
            messagebox.showinfo("成功", f"环境 {env_name} 已成功删除！")
    except subprocess.CalledProcessError as e:
        log_message(f"删除环境时出错：{e.stderr}")
        messagebox.showerror("错误", f"删除环境时出错：{e.stderr}")

def list_conda_envs():
    # 执行 conda env list 命令
    try:
        log_message("正在获取环境列表...")
        result = subprocess.run(["conda", "env", "list"], capture_output=True, text=True, check=True)
        env_list = result.stdout.strip().split("\n")[2:]  # 跳过前两行（标题行）

        # 创建 PrettyTable
        table = PrettyTable()
        table.field_names = ["环境名称", "路径"]
        
        for env in env_list:
            env = env.strip()
            if env:  # 确保不是空行
                parts = env.split()
                if len(parts) == 2:  # 确保行格式正确
                    env_name, env_path = parts
                    table.add_row([env_name, env_path])
                else:
                    log_message(f"跳过无效行: {env}")

        # 清空表格显示区域
        table_display.config(state="normal")
        table_display.delete("1.0", tk.END)
        table_display.insert("end", table.get_string())
        table_display.config(state="disabled")
    except subprocess.CalledProcessError as e:
        log_message(f"获取环境列表时出错：{e.stderr}")
        messagebox.showerror("错误", f"获取环境列表时出错：{e.stderr}")

# 创建主窗口
root = tk.Tk()
root.title("Anaconda 环境管理工具")

# 创建创建环境的输入框和标签
tk.Label(root, text="环境名称:").grid(row=0, column=0, padx=10, pady=10)
env_name_entry = tk.Entry(root)
env_name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="环境路径 (可选):").grid(row=1, column=0, padx=10, pady=10)
env_path_entry = tk.Entry(root)
env_path_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Python 版本 (可选):").grid(row=2, column=0, padx=10, pady=10)
python_version_entry = tk.Entry(root)
python_version_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="要安装的包 (用空格分隔):").grid(row=3, column=0, padx=10, pady=10)
packages_entry = tk.Entry(root)
packages_entry.grid(row=3, column=1, padx=10, pady=10)

# 创建创建环境的按钮
create_button = tk.Button(root, text="创建环境", command=create_conda_env)
create_button.grid(row=4, column=0, columnspan=2, pady=20)

# 创建删除环境的输入框和标签
tk.Label(root, text="删除环境名称:").grid(row=5, column=0, padx=10, pady=10)
delete_env_name_entry = tk.Entry(root)
delete_env_name_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="删除环境路径 (可选):").grid(row=6, column=0, padx=10, pady=10)
delete_env_path_entry = tk.Entry(root)
delete_env_path_entry.grid(row=6, column=1, padx=10, pady=10)

# 创建删除环境的按钮
delete_button = tk.Button(root, text="删除环境", command=delete_conda_env)
delete_button.grid(row=7, column=0, columnspan=2, pady=20)

# 创建列出所有环境的按钮
list_button = tk.Button(root, text="列出所有环境", command=list_conda_envs)
list_button.grid(row=8, column=0, columnspan=2, pady=20)

# 创建表格显示区域
table_display = tk.Text(root, height=10, width=60, state="disabled")
table_display.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# 创建日志显示区域
log_display = tk.Text(root, height=10, width=60, state="disabled")
log_display.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

# 运行主循环
root.mainloop()