import streamlit as st

def show():
    st.title("💰 Welcome to Your Personal Financial Dashboard")
    
    st.write("""
    Take control of your finances with our comprehensive financial management tool. 
    Track your income, expenses, and investments all in one place.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Features")
        st.markdown("""
        - 📊 Real-time financial overview
        - 💰 Income and expense tracking
        - 📈 Visual financial reports
        - 🔄 Recurring payments management
        - 📱 Access anywhere, anytime
        """)
        
        st.markdown("---")
        st.subheader("Get Started")
        
        # Center the buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login to Your Account", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        with col2:
            if st.button("📝 Create New Account", type="primary", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
    
    with col2:
        st.subheader("Why Choose Us?")
        
        features = [
            {"icon": "🔒", "title": "Secure", "desc": "Bank-level security for your data"},
            {"icon": "📱", "title": "Accessible", "desc": "Use on any device, anywhere"},
            {"icon": "📊", "title": "Insightful", "desc": "Powerful analytics and reports"},
            {"icon": "🔄", "title": "Automated", "desc": "Save time with automation"}
        ]
        
        for feature in features:
            with st.container(border=True):
                st.markdown(f"#### {feature['icon']} {feature['title']}")
                st.caption(feature['desc'])
    
    st.markdown("---")
    
    # Add a demo section
    st.subheader("See It In Action")
    st.image("https://via.placeholder.com/800x400?text=Dashboard+Preview", use_container_width=True)
    st.caption("*Screenshot of the dashboard interface*")

# This will be called from the main app
if __name__ == "__main__":
    show()
