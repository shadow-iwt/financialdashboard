import streamlit as st

def show():
    st.title("📞 Contact Us")
    
    st.write("""
    We'd love to hear from you! Whether you have a question about features, need assistance,
    or want to provide feedback, our team is here to help.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Get in Touch")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Email Address")
            subject = st.selectbox(
                "Subject",
                ["General Inquiry", "Technical Support", "Feature Request", "Feedback", "Other"]
            )
            message = st.text_area("Your Message", height=150)
            
            submitted = st.form_submit_button("Send Message")
            if submitted:
                if name and email and message:
                    # In a real app, you would handle the form submission here
                    st.success("Thank you for your message! We'll get back to you soon.")
                else:
                    st.warning("Please fill in all required fields.")
    
    with col2:
        st.subheader("Our Information")
        
        st.markdown("""
        **📍 Address**  
        123 Finance Street  
        New York, NY 10001  
        United States
        
        **📞 Phone**  
        +1 (555) 123-4567
        
        **✉️ Email**  
        support@financialdashboard.com
        
        **🕒 Business Hours**  
        Monday - Friday: 9:00 AM - 6:00 PM EST  
        Saturday: 10:00 AM - 4:00 PM EST  
        Sunday: Closed
        """)
    
    st.markdown("---")
    
    st.subheader("Frequently Asked Questions")
    
    faqs = [
        {
            "question": "Is my financial data secure?",
            "answer": "Yes, we use bank-level encryption and follow strict security protocols to protect your data."
        },
        {
            "question": "Can I access my dashboard from multiple devices?",
            "answer": "Absolutely! Your dashboard is accessible from any device with an internet connection."
        },
        {
            "question": "How do I reset my password?",
            "answer": "Click on 'Forgot Password' on the login page and follow the instructions sent to your email."
        },
        {
            "question": "Is there a mobile app available?",
            "answer": "Our web app is fully responsive and works on mobile browsers. We're also working on dedicated mobile apps."
        }
    ]
    
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])

if __name__ == "__main__":
    show()
