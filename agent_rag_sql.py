# ===================== 零售数据智能分析Agent（极简稳定版，100%无解析错误） =====================
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# ===================== 全局配置 =====================
load_dotenv()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 千问大模型 =====================
from langchain_community.chat_models import ChatTongyi

llm = ChatTongyi(
    model="qwen-turbo",
    api_key="sk-ws-H.REHEDPD.hSR7.MEUCIDfrL4Ck5elCd23xLNE4Cgfmg9UB_UVRpfNQs6b354RmAiEArEScxrIIUM6j67KJ04D6koKMezN1AHgRHQgOSwTlCuU",
    temperature=0
)


# ===================== 工具函数（手动调用，零解析错误） =====================
def execute_sql(query):
    """执行SQL查询"""
    conn = sqlite3.connect("retail_sales.db")
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def generate_chart(df, chart_type, title):
    """生成图表"""
    x_col, y_col = df.columns[0], df.columns[1]
    plt.figure(figsize=(10, 6))
    if chart_type == "bar":
        plt.bar(df[x_col], df[y_col])
    elif chart_type == "line":
        plt.plot(df[x_col], df[y_col], marker="o")
    elif chart_type == "pie":
        plt.pie(df[y_col], labels=df[x_col], autopct="%1.1f%%")
    plt.title(title, fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_name = f"{title}.png"
    plt.savefig(save_name, dpi=300)
    plt.close()
    return save_name


# ===================== 主对话循环（完全手动控制，零错误） =====================
if __name__ == "__main__":
    print("🤖 零售数据智能分析Agent启动成功！")
    print("💡 支持：自然语言查数据、生成图表 | 输入 退出 结束\n")

    while True:
        user_question = input("请输入你的问题：")
        if user_question == "退出":
            print("👋 程序结束！")
            break

        # 步骤1：让大模型生成SQL
        sql_prompt = f"""
        用户问题：{user_question}
        零售销售数据表名：sales_data
        字段：Order_Date(订单日期), Sales(销售额), Region(地区), Category(品类), Segment(客户类型)
        只输出纯SQL语句，不要任何解释、不要任何格式、不要引号，直接输出SQL：
        """
        sql_result = llm.invoke(sql_prompt).content.strip()
        print(f"🔍 生成SQL：{sql_result}")

        # 步骤2：执行SQL
        try:
            df = execute_sql(sql_result)
            print("✅ 查询成功，数据：")
            print(df.to_string(index=False))
        except Exception as e:
            print(f"❌ SQL错误：{e}")
            continue

        # 步骤3：判断是否需要绘图
        chart_keywords = ["图", "图表", "柱状图", "折线图", "饼图", "可视化"]
        need_chart = any(k in user_question for k in chart_keywords)

        if need_chart:
            # 自动判断图表类型
            chart_type = "bar"
            if "折线" in user_question:
                chart_type = "line"
            if "饼" in user_question:
                chart_type = "pie"

            title = user_question.replace("生成", "").replace("的", "")
            img_name = generate_chart(df, chart_type, title)
            print(f"🖼️ 图表已生成：{img_name}")

        # 步骤4：大模型整理分析结果
        analysis_prompt = f"""
        用户问题：{user_question}
        查询到的数据：
        {df.to_string(index=False)}

        结合数据给出专业的零售数据分析结论，条理清晰，中文回答：
        """
        final_answer = llm.invoke(analysis_prompt).content
        print("\n📊 最终分析结果：")
        print(final_answer)
        print("-" * 70)