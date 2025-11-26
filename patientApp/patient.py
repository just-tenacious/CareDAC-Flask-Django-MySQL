from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_cors import CORS
from functools import wraps
import os
import requests
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# ==================== APP CONFIGURATION ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(app, supports_credentials=True)

# Django API URL (for backend integration)
DJANGO_API_URL = os.getenv('DJANGO_API_URL', 'http://localhost:8000/api')



# @app.route('/patient/signup', method=['GET','POST'])
@app.route('/')
def signup():
    """
    Registration page with OTP flow
    Flow: Register → OTP → Who-need-care → Member-details → Patient-details → Index
    """
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('fullName'),
            'dob': request.form.get('dob'),
            'email': request.form.get('email'),
            'mobile': request.form.get('mobile'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender')
        }
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/register', method='POST', data=data)
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'signup'
        #     session['user_email'] = data['email']
        #     session['temp_user_id'] = response.get('user_id')
        #     
        #     # Send OTP
        #     otp_sent = make_api_request('auth/send-otp', method='POST', data={
        #         'email': data['email'],
        #         'type': 'signup'
        #     })
        #     
        #     if otp_sent:
        #         flash('Please verify your email with OTP', 'success')
        #         return redirect(url_for('otp_verify', **{'from': 'signup'}))
        #     else:
        #         flash('Error sending OTP', 'error')
        # else:
        #     flash('Registration failed. Email may already exist.', 'error')
        
        # For demo (remove in production):
        session['auth_flow'] = 'signup'
        session['user_email'] = data['email']
        session['signup_data'] = data
        return redirect(url_for('otp_verify', **{'from': 'signup'}))
    return render_template('authPages/signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page with OTP flow
    Flow: Login → OTP → Dashboard/Index
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/login', method='POST', data={
        #     'email': email,
        #     'password': password
        # })
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'login'
        #     session['user_email'] = email
        #     session['temp_user_id'] = response.get('user_id')
        #     
        #     # Send OTP
        #     otp_sent = make_api_request('auth/send-otp', method='POST', data={
        #         'email': email,
        #         'type': 'login'
        #     })
        #     
        #     if otp_sent:
        #         flash('OTP sent to your email', 'success')
        #         return redirect(url_for('otp_verify', **{'from': 'login'}))
        #     else:
        #         flash('Error sending OTP', 'error')
        # else:
        #     flash('Invalid credentials', 'error')
        
        # For demo (remove in production):
        session['auth_flow'] = 'login'
        session['user_email'] = email
        return redirect(url_for('otp_verify', **{'from': 'login'}))
    
    return render_template('authPages/login.html')

@app.route('/otp')
def otp_verify():
    """
    OTP verification page - handles multiple flows
    Flows:
    - login: OTP → Index
    - signup: OTP → Who-need-care
    - forgot-password: OTP → Reset-password
    """
    otp_from = request.args.get('from', 'login')
    
    # Store flow type in session
    if otp_from in ['login', 'signup', 'forgot-password']:
        session['otp_type'] = otp_from
    
    return render_template('authPages/otp-verification.html', otp_from=otp_from)


@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    """
    API endpoint to verify OTP
    Called from frontend JavaScript
    """
    data = request.get_json()
    otp = data.get('otp')
    email = data.get('email')
    otp_type = data.get('type')
    
    # BACKEND INTEGRATION:
    # response = make_api_request('auth/verify-otp', method='POST', data={
    #     'email': email,
    #     'otp': otp,
    #     'type': otp_type
    # })
    # 
    # if response and response.get('success'):
    #     if otp_type == 'login':
    #         session['user_id'] = response.get('user_id')
    #         session['auth_token'] = response.get('token')
    #         session['is_authenticated'] = True
    #         session.pop('auth_flow', None)
    #         return jsonify({'success': True, 'redirect': '/'})
    #     
    #     elif otp_type == 'signup':
    #         session['user_id'] = response.get('user_id')
    #         session['is_verified'] = True
    #         return jsonify({'success': True, 'redirect': '/whoneedcare'})
    #     
    #     elif otp_type == 'forgot-password':
    #         session['reset_token'] = response.get('reset_token')
    #         return jsonify({'success': True, 'redirect': '/reset-pass'})
    # 
    # return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
    
    # For demo (remove in production):
    return jsonify({'success': True, 'redirect': '/whoneedcare' if otp_type == 'signup' else '/'})


@app.route('/api/resend-otp', methods=['POST'])
def api_resend_otp():
    """
    API endpoint to resend OTP
    """
    data = request.get_json()
    email = data.get('email')
    otp_type = data.get('type')
    
    # BACKEND INTEGRATION:
    # response = make_api_request('auth/resend-otp', method='POST', data={
    #     'email': email,
    #     'type': otp_type
    # })
    # 
    # if response and response.get('success'):
    #     return jsonify({'success': True, 'message': 'OTP resent successfully'})
    # 
    # return jsonify({'success': False, 'message': 'Failed to resend OTP'}), 400
    
    # For demo:
    return jsonify({'success': True, 'message': 'OTP resent successfully'})


@app.route('/forget-pass', methods=['GET', 'POST'])
def forget_password():
    """
    Forgot password page
    Flow: Forget-password → OTP → Reset-password → Login
    """
    if request.method == 'POST':
        email = request.form.get('email')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/forgot-password', method='POST', data={
        #     'email': email
        # })
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'forgot-password'
        #     session['user_email'] = email
        #     flash('OTP sent to your email', 'success')
        #     return redirect(url_for('otp_verify', **{'from': 'forgot-password'}))
        # else:
        #     flash('Email not found', 'error')
        
        # For demo:
        session['auth_flow'] = 'forgot-password'
        session['user_email'] = email
        return redirect(url_for('otp_verify', **{'from': 'forgot-password'}))
    
    return render_template('authPages/forget-password.html')


@app.route('/reset-pass', methods=['GET', 'POST'])
def reset_password():
    """
    Reset password page
    Requires valid reset token from OTP verification
    """
    # Verify user came from OTP verification
    # if 'reset_token' not in session:
    #     flash('Invalid or expired reset link', 'error')
    #     return redirect(url_for('forget_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        email = session.get('user_email')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/reset-password', method='POST', data={
        #     'email': email,
        #     'password': password,
        #     'token': session.get('reset_token')
        # })
        # 
        # if response and response.get('success'):
        #     session.pop('reset_token', None)
        #     session.pop('auth_flow', None)
        #     session.pop('user_email', None)
        #     flash('Password reset successfully! Please login.', 'success')
        #     return redirect(url_for('login'))
        # else:
        #     flash('Error resetting password', 'error')
        
        # For demo:
        flash('Password reset successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('authPages/reset-password.html')


@app.route('/whoneedcare', methods=['GET', 'POST'])
# @verify_flow('signup')  # Uncomment in production
def who_need_care():
    """
    Multi-step form: Who needs care
    Flow after signup: Who-need-care → Member-details → Patient-details → Index
    """
    if request.method == 'POST':
        data = request.get_json()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('care-needs', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'who_needs_care': data.get('whoNeedsCare'),
        #     'age': data.get('age'),
        #     'postcode': data.get('postcode'),
        #     'help_option': data.get('helpOption'),
        #     'services': data.get('services')
        # })
        # 
        # if response and response.get('success'):
        #     session['care_need_id'] = response.get('care_need_id')
        #     return jsonify({'success': True, 'redirect': '/enter-member-details'})
        # 
        # return jsonify({'success': False}), 400
        
        # For demo:
        return jsonify({'success': True})
    
    return render_template('authPages/who-need-care.html')



@app.route("/enter-member-details", methods=["GET", "POST"])
# @login_required  # Uncomment in production
def enter_member_details():
    """
    Enter member details form
    Part of signup onboarding flow
    """
    if request.method == "POST":
        data = request.form.to_dict()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('members', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'care_need_id': session.get('care_need_id'),
        #     'full_name': data.get('fullName'),
        #     'dob': data.get('dob'),
        #     'phone': data.get('phone'),
        #     'gender': data.get('gender'),
        #     'address1': data.get('address1'),
        #     'address2': data.get('address2'),
        #     'country': data.get('country'),
        #     'state': data.get('state'),
        #     'city': data.get('city'),
        #     'pincode': data.get('pincode')
        # })
        # 
        # if response and response.get('success'):
        #     session['member_id'] = response.get('member_id')
        #     return redirect(url_for('enter_patient_details'))
        # else:
        #     flash('Error saving member details', 'error')
        
        print("Received member details:", data)
        return redirect(url_for('enter_patient_details'))
    
    return render_template("authPages/enter_member_details.html") 


@app.route("/enter-patient-details", methods=["GET", "POST"])
# @login_required  # Uncomment in production
def enter_patient_details():
    """
    Enter patient details form
    Final step of signup onboarding flow
    """
    if request.method == "POST":
        data = request.form.to_dict()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('patients', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'member_id': session.get('member_id'),
        #     'address1': data.get('address1'),
        #     'address2': data.get('address2'),
        #     'country': data.get('country'),
        #     'state': data.get('state'),
        #     'city': data.get('city'),
        #     'pincode': data.get('pincode')
        # })
        # 
        # if response and response.get('success'):
        #     # Complete onboarding
        #     session['onboarding_completed'] = True
        #     session.pop('auth_flow', None)
        #     flash('Registration completed successfully!', 'success')
        #     return redirect(url_for('index'))
        # else:
        #     flash('Error saving patient details', 'error')
        
        print("Patient details received:", data)
        return redirect(url_for('success'))
    
    return render_template("authPages/enter_patient_details.html")

# @app.route("/success")
# def success():
#     """
#     Generic success page
#     """
#     message = request.args.get('message', 'Registraion completed successfully!')
    
#     return render_template('authPages/login.html', message=message)
#     # return message


if __name__ == '__main__':
    print('\n\tpatient\n')
    app.run(
        debug=True,
        port=5002,
        host='0.0.0.0'
    )