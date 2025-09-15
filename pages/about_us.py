import streamlit as st

def show():
    st.title("ℹ️ About Us")
    
    st.write("""
    ## Our Mission
    At Financial Dashboard, we believe that everyone deserves financial clarity and control. 
    Our mission is to provide intuitive tools that help you understand and manage your personal 
    finances with confidence.
    """)
    
    st.markdown("---")
    
    st.subheader("Our Story")
    st.write("""
    Founded in 2024, Financial Dashboard was born out of a simple idea: financial management 
    should be accessible, understandable, and empowering for everyone. Our team of financial 
    experts and tech enthusiasts came together to create a solution that makes personal 
    finance management both powerful and easy to use.
    """)
    
    st.markdown("---")
    
    st.subheader("Meet the Team")
    
    team = [
        {"name": "John Doe", "role": "CEO & Founder", "bio": "Financial expert with 10+ years in fintech"},
        {"name": "Jane Smith", "role": "Lead Developer", "bio": "Full-stack developer specializing in financial applications"},
        {"name": "Alex Johnson", "role": "UX Designer", "bio": "Passionate about creating intuitive user experiences"},
        {"name": "Sarah Williams", "role": "Financial Analyst", "bio": "Helping users make better financial decisions"}
    ]
    
    cols = st.columns(2)
    for idx, member in enumerate(team):
        with cols[idx % 2]:
            with st.container(border=True):
                st.subheader(member["name"])
                st.caption(f"_{member['role']}_")
                st.write(member["bio"])
    
    st.markdown("---")
    st.subheader("Our Values")
    
    values = [
        "🔍 Transparency in everything we do",
        "🛡️ Security and privacy first",
        "💡 Innovation for better financial health",
        "🤝 Customer success is our success"
    ]
    
    for value in values:
        st.write(f"- {value}")

if __name__ == "__main__":
    show()
