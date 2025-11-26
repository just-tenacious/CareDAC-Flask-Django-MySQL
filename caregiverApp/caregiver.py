from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
import requests
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# =============================================================================
# DJANGO API CONFIGURATION
# =============================================================================
DJANGO_API_BASE = "https://untranscendental-psychodiagnostic-nixon.ngrok-free.dev"
DJANGO_CAREGIVER_ENDPOINT = f"{DJANGO_API_BASE}/caregiver/caregiver_info/"
DJANGO_OTP_ENDPOINT = f"{DJANGO_API_BASE}/otp_verification/"
DJANGO_LOGIN_ENDPOINT = f"{DJANGO_API_BASE}/caregiver_login/"
DJANGO_TIMEOUT = 30

# Common headers for Django API (JSON)
DJANGO_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'ngrok-skip-browser-warning': 'true'
}

# =============================================================================
# UPLOAD CONFIGURATION
# =============================================================================
UPLOAD_FOLDER = 'static/uploads/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Age configuration
MIN_AGE = 18


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename):
    """Generate unique filename to avoid conflicts"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_name = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return unique_name


def save_profile_picture(file):
    """
    Save uploaded profile picture and return filename
    Returns: filename if successful, None if failed
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    try:
        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"✅ Profile picture saved: {filename}")
        return filename
    
    except Exception as e:
        print(f"❌ Failed to save profile picture: {e}")
        return None


def calculate_age(dob_string):
    """Calculate age from date of birth string (YYYY-MM-DD)"""
    try:
        dob = datetime.strptime(dob_string, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None


def validate_signup_data(data):
    """Validate signup form data and return errors dict"""
    errors = {}
    
    full_name = data.get('fullName', '').strip()
    if not full_name:
        errors['fullName'] = 'Full name is required'
    elif len(full_name) < 2:
        errors['fullName'] = 'Full name must be at least 2 characters'
    
    email = data.get('email', '').strip().lower()
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email or '.' not in email:
        errors['email'] = 'Please enter a valid email address'
    
    phone = data.get('mobile', '').strip()
    phone_digits = ''.join(filter(str.isdigit, phone))
    if not phone:
        errors['mobile'] = 'Mobile number is required'
    elif len(phone_digits) < 10:
        errors['mobile'] = 'Mobile number must be at least 10 digits'
    
    password = data.get('password', '')
    if not password:
        errors['password'] = 'Password is required'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters'
    
    confirm_password = data.get('confirmPassword', '')
    if not confirm_password:
        errors['confirmPassword'] = 'Please confirm your password'
    elif password != confirm_password:
        errors['confirmPassword'] = 'Passwords do not match'
    
    dob = data.get('dob', '')
    if not dob:
        errors['dob'] = 'Date of birth is required'
    else:
        age = calculate_age(dob)
        if age is None:
            errors['dob'] = 'Invalid date format'
        elif age < MIN_AGE:
            errors['dob'] = f'You must be at least {MIN_AGE} years old'
        elif age > 120:
            errors['dob'] = 'Please enter a valid date of birth'
    
    terms = data.get('terms', '')
    if terms != 'true' and terms != True:
        errors['terms'] = 'You must agree to the terms and conditions'
    
    return errors


# =============================================================================
# PAGE ROUTES
# =============================================================================
@app.route('/')
def index():
    if session.get('is_logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup')
def signup():
    return render_template('authPages/signup.html')


@app.route('/login')
def login():
    if session.get('is_logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('authPages/login.html')


@app.route('/otp')
def otp():
    if 'signup_data' not in session and 'login_data' not in session:
        return redirect(url_for('signup'))
    return render_template('authPages/otp-verification.html')


@app.route('/dashboard')
def dashboard():
    user = session.get('user_data', {})
    if not user:
        return redirect(url_for('login'))
    
    # Get profile picture URL
    profile_pic = user.get('profile_pic')
    if profile_pic:
        profile_pic_url = f"/uploads/profiles/{profile_pic}"
    else:
        profile_pic_url = "https://via.placeholder.com/100x100?text=No+Image"
    
    return f"""
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 50px; text-align: center; background: #f5f5f5; }}
            .card {{ background: white; max-width: 500px; margin: 50px auto; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
            h1 {{ color: #1e40af; margin-bottom: 20px; }}
            .success {{ color: #22c55e; font-size: 1.2rem; margin-bottom: 20px; }}
            .info {{ color: #666; margin: 10px 0; }}
            .info strong {{ color: #333; }}
            a {{ color: #1e40af; text-decoration: none; }}
            .logout-btn {{ display: inline-block; margin-top: 20px; padding: 10px 30px; background: #dc3545; color: white; border-radius: 8px; }}
            .logout-btn:hover {{ background: #c82333; color: white; }}
            .profile-pic {{ width: 100px; height: 100px; border-radius: 50%; object-fit: cover; margin-bottom: 20px; border: 3px solid #1e40af; }}
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{profile_pic_url}" alt="Profile" class="profile-pic">
            <h1>🎉 Welcome!</h1>
            <p class="success">Login successful!</p>
            <p class="info"><strong>Name:</strong> {user.get('full_name', 'N/A')}</p>
            <p class="info"><strong>Email:</strong> {user.get('email', 'N/A')}</p>
            <p class="info"><strong>Caregiver ID:</strong> {user.get('caregiver_id', 'N/A')}</p>
            <p class="info"><strong>Account Status:</strong> {'Verified ✅' if user.get('acc_status') == 1 else 'Not Verified ❌'}</p>
            <a href="/logout" class="logout-btn">Logout</a>
        </div>
    </body>
    </html>
    """


@app.route('/logout')
def logout():
    """Clear session and redirect to login"""
    session.clear()
    return redirect(url_for('login'))


# =============================================================================
# SERVE UPLOADED FILES
# =============================================================================
@app.route('/uploads/profiles/<filename>')
def serve_profile_pic(filename):
    """Serve uploaded profile pictures"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# =============================================================================
# API: LOGIN
# =============================================================================
@app.route('/api/login', methods=['POST'])
def api_login():
    """Login caregiver via Django API"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email is required', 'errors': {'email': 'Email is required'}}), 400
        
        if not password:
            return jsonify({'success': False, 'message': 'Password is required', 'errors': {'password': 'Password is required'}}), 400
        
        login_payload = {
            'email': email,
            'password': password
        }
        
        print("\n" + "=" * 60)
        print("🔐 LOGIN REQUEST TO DJANGO API")
        print("=" * 60)
        print(f"URL: {DJANGO_LOGIN_ENDPOINT}")
        print(f"Payload: {login_payload}")
        
        login_response = requests.post(
            DJANGO_LOGIN_ENDPOINT,
            json=login_payload,
            headers=DJANGO_HEADERS,
            timeout=DJANGO_TIMEOUT
        )
        
        print(f"Response Status: {login_response.status_code}")
        print(f"Response Body: {login_response.text}")
        print("=" * 60 + "\n")
        
        try:
            login_data = login_response.json()
        except:
            print("❌ Failed to parse JSON response")
            return jsonify({'success': False, 'message': 'Server error. Please try again.'}), 500
        
        if isinstance(login_data, list):
            if len(login_data) > 0:
                login_data = login_data[0]
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password',
                    'errors': {'email': 'No account found with this email'}
                }), 401
        
        if login_response.status_code >= 400:
            error_msg = login_data.get('message', login_data.get('error', login_data.get('detail', 'Login failed')))
            return jsonify({
                'success': False,
                'message': error_msg,
                'errors': {'password': 'Invalid email or password'}
            }), 401
        
        user_info = login_data.get('user') or login_data.get('caregiver') or login_data.get('data') or login_data
        
        caregiver_id = (
            user_info.get('caregiver_id') or 
            user_info.get('id') or 
            user_info.get('user_id') or
            login_data.get('caregiver_id')
        )
        
        acc_status = user_info.get('acc_status', 1)
        full_name = user_info.get('full_name', user_info.get('name', ''))
        phone_no = user_info.get('phone_no', user_info.get('phone', ''))
        profile_pic = user_info.get('profile_pic', None)
        
        print(f"✅ Parsed user data:")
        print(f"   Caregiver ID: {caregiver_id}")
        print(f"   Full Name: {full_name}")
        print(f"   Account Status: {acc_status}")
        print(f"   Profile Pic: {profile_pic}")
        
        if acc_status == 0:
            print("⚠️ Account not verified (acc_status=0). Sending OTP...")
            
            session['login_data'] = {
                'email': email,
                'caregiver_id': caregiver_id,
                'full_name': full_name,
                'phone_no': phone_no,
                'profile_pic': profile_pic
            }
            
            try:
                otp_response = requests.post(
                    DJANGO_OTP_ENDPOINT,
                    json={'email': email},
                    headers=DJANGO_HEADERS,
                    timeout=DJANGO_TIMEOUT
                )
                print(f"OTP Response: {otp_response.status_code} - {otp_response.text}")
            except Exception as e:
                print(f"OTP send error: {e}")
            
            return jsonify({
                'success': True,
                'message': 'Account not verified. Please verify with OTP.',
                'requires_verification': True,
                'redirect_url': '/otp?from=login'
            }), 200
        
        else:
            print("✅ Account verified (acc_status=1). Login successful!")
            
            session['user_data'] = {
                'caregiver_id': caregiver_id,
                'full_name': full_name,
                'email': email,
                'phone_no': phone_no,
                'profile_pic': profile_pic,
                'acc_status': acc_status,
                'is_authenticated': True
            }
            session['is_logged_in'] = True
            
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': '/dashboard'
            }), 200
        
    except requests.exceptions.Timeout:
        print("❌ Timeout")
        return jsonify({'success': False, 'message': 'Server timeout. Please try again.'}), 504
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        return jsonify({'success': False, 'message': 'Unable to connect to server.'}), 503
    
    except Exception as e:
        print(f"❌ Login Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'An unexpected error occurred.'}), 500


# =============================================================================
# API: SIGNUP - Step 1 (Validate & Send OTP + Save Profile Pic)
# =============================================================================
@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Step 1: Validate signup data, save profile pic, call Django OTP API"""
    try:
        # Get form data
        form_data = {
            'fullName': request.form.get('fullName', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'mobile': request.form.get('mobile', '').strip(),
            'password': request.form.get('password', ''),
            'confirmPassword': request.form.get('confirmPassword', ''),
            'dob': request.form.get('dob', ''),
            'gender': request.form.get('gender', 'Male'),
            'terms': request.form.get('terms', 'false')
        }
        
        # Validate form data
        errors = validate_signup_data(form_data)
        
        if errors:
            return jsonify({
                'success': False,
                'message': 'Please fix the errors below',
                'errors': errors
            }), 400
        
        # ============================================================
        # HANDLE PROFILE PICTURE UPLOAD
        # ============================================================
        profile_pic_filename = None
        
        if 'profilePic' in request.files:
            profile_file = request.files['profilePic']
            
            if profile_file and profile_file.filename != '':
                # Validate file type
                if not allowed_file(profile_file.filename):
                    return jsonify({
                        'success': False,
                        'message': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP',
                        'errors': {'profilePic': 'Invalid file type'}
                    }), 400
                
                # Save the file
                profile_pic_filename = save_profile_picture(profile_file)
                
                if profile_pic_filename:
                    print(f"📸 Profile picture uploaded: {profile_pic_filename}")
                else:
                    print("⚠️ Profile picture upload failed, continuing without it")
        
        # Check if email already exists
        try:
            response = requests.get(DJANGO_CAREGIVER_ENDPOINT, headers=DJANGO_HEADERS, timeout=10)
            if response.status_code == 200:
                caregivers = response.json()
                if any(c.get('email', '').lower() == form_data['email'] for c in caregivers):
                    # Delete uploaded profile pic if email exists
                    if profile_pic_filename:
                        try:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic_filename))
                        except:
                            pass
                    
                    return jsonify({
                        'success': False,
                        'message': 'This email is already registered',
                        'errors': {'email': 'This email is already registered. Please login instead.'}
                    }), 400
        except Exception as e:
            print(f"⚠️ Email check warning: {e}")
        
        # Send OTP
        otp_payload = {'email': form_data['email']}
        
        print("\n" + "=" * 60)
        print("📤 SENDING OTP REQUEST TO DJANGO API")
        print("=" * 60)
        print(f"URL: {DJANGO_OTP_ENDPOINT}")
        print(f"Payload: {otp_payload}")
        
        otp_response = requests.post(
            DJANGO_OTP_ENDPOINT,
            json=otp_payload,
            headers=DJANGO_HEADERS,
            timeout=DJANGO_TIMEOUT
        )
        
        print(f"Response Status: {otp_response.status_code}")
        print(f"Response Body: {otp_response.text}")
        print("=" * 60 + "\n")
        
        if otp_response.status_code in [200, 201]:
            otp_data = otp_response.json()
            
            # Store signup data in session (including profile pic filename)
            session['signup_data'] = {
                'full_name': form_data['fullName'],
                'email': form_data['email'],
                'phone_no': form_data['mobile'],
                'password': form_data['password'],
                'dob': form_data['dob'],
                'gender': form_data['gender'],
                'profile_pic': profile_pic_filename  # ← STORE FILENAME
            }
            
            if 'otp_id' in otp_data:
                session['otp_id'] = otp_data['otp_id']
            
            print("✅ OTP sent successfully to:", form_data['email'])
            print(f"📸 Profile pic stored in session: {profile_pic_filename}")
            
            return jsonify({
                'success': True,
                'message': otp_data.get('message', 'OTP sent to your email!'),
                'redirect_url': '/otp?from=signup'
            }), 200
        
        else:
            # OTP failed - delete uploaded profile pic
            if profile_pic_filename:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic_filename))
                except:
                    pass
            
            error_message = 'Failed to send OTP. Please try again.'
            try:
                error_data = otp_response.json()
                error_message = error_data.get('message', error_message)
            except:
                pass
            
            return jsonify({
                'success': False,
                'message': error_message
            }), 400
        
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'message': 'Server timeout. Please try again.'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'message': 'Unable to connect to server.'}), 503
    except Exception as e:
        print(f"❌ Signup Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'An unexpected error occurred.'}), 500


# =============================================================================
# API: VERIFY OTP - Step 2 (Create Caregiver with Profile Pic)
# =============================================================================
@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    """Verify OTP via Django API, if correct create/verify caregiver"""
    try:
        data = request.get_json()
        entered_otp = data.get('otp', '').strip()
        email = data.get('email', '').strip().lower()
        otp_type = data.get('type', 'signup')
        
        signup_data = session.get('signup_data')
        login_data = session.get('login_data')
        
        if not signup_data and not login_data:
            return jsonify({
                'success': False,
                'message': 'Session expired. Please try again.'
            }), 400
        
        if not entered_otp or len(entered_otp) != 4:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid 4-digit OTP'
            }), 400
        
        verify_payload = {
            'email': email or (signup_data or login_data).get('email'),
            'otp': entered_otp
        }
        
        if 'otp_id' in session:
            verify_payload['otp_id'] = session['otp_id']
        
        print("\n" + "=" * 60)
        print("🔐 VERIFYING OTP VIA DJANGO API")
        print("=" * 60)
        print(f"Payload: {verify_payload}")
        
        verify_response = requests.post(
            DJANGO_OTP_ENDPOINT,
            json=verify_payload,
            headers=DJANGO_HEADERS,
            timeout=DJANGO_TIMEOUT
        )
        
        print(f"Response: {verify_response.status_code} - {verify_response.text}")
        print("=" * 60 + "\n")
        
        if verify_response.status_code in [200, 201]:
            verify_data = verify_response.json()
            is_verified = verify_data.get('verified', verify_data.get('success', True))
            
            if is_verified:
                if otp_type == 'signup' and signup_data:
                    # ============================================================
                    # CREATE CAREGIVER WITH PROFILE PIC
                    # ============================================================
                    profile_pic = signup_data.get('profile_pic')  # ← GET FROM SESSION
                    
                    caregiver_payload = {
                        'full_name': signup_data['full_name'],
                        'email': signup_data['email'],
                        'phone_no': signup_data['phone_no'],
                        'password': signup_data['password'],
                        'dob': signup_data['dob'],
                        'gender': signup_data['gender'],
                        'profile_pic': profile_pic,  # ← INCLUDE PROFILE PIC
                        'acc_status': 1
                    }
                    
                    print("📤 Creating caregiver with profile pic...")
                    print(f"   Profile Pic: {profile_pic}")
                    
                    caregiver_response = requests.post(
                        DJANGO_CAREGIVER_ENDPOINT,
                        json=caregiver_payload,
                        headers=DJANGO_HEADERS,
                        timeout=DJANGO_TIMEOUT
                    )
                    
                    print(f"Response: {caregiver_response.status_code} - {caregiver_response.text}")
                    
                    if caregiver_response.status_code in [200, 201]:
                        caregiver_data = caregiver_response.json()
                        
                        session.pop('signup_data', None)
                        session.pop('otp_id', None)
                        
                        session['user_data'] = {
                            'caregiver_id': caregiver_data.get('caregiver_id'),
                            'full_name': signup_data['full_name'],
                            'email': signup_data['email'],
                            'phone_no': signup_data['phone_no'],
                            'profile_pic': profile_pic,  # ← STORE IN SESSION
                            'acc_status': 1,
                            'is_authenticated': True
                        }
                        session['is_logged_in'] = True
                        
                        print("🎉 Caregiver created successfully with profile pic!")
                        
                        return jsonify({
                            'success': True,
                            'message': 'Account created successfully!',
                            'redirect_url': '/dashboard'
                        }), 200
                    
                    else:
                        # Delete profile pic if caregiver creation failed
                        if profile_pic:
                            try:
                                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
                            except:
                                pass
                        
                        return jsonify({
                            'success': False,
                            'message': 'Failed to create account.'
                        }), 400
                
                elif otp_type == 'login' and login_data:
                    session.pop('login_data', None)
                    session.pop('otp_id', None)
                    
                    session['user_data'] = {
                        'caregiver_id': login_data.get('caregiver_id'),
                        'full_name': login_data.get('full_name', ''),
                        'email': login_data.get('email'),
                        'phone_no': login_data.get('phone_no', ''),
                        'profile_pic': login_data.get('profile_pic'),
                        'acc_status': 1,
                        'is_authenticated': True
                    }
                    session['is_logged_in'] = True
                    
                    print("🎉 Account verified and logged in!")
                    
                    return jsonify({
                        'success': True,
                        'message': 'Account verified successfully!',
                        'redirect_url': '/dashboard'
                    }), 200
                
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Session data not found.'
                    }), 400
            
            else:
                return jsonify({
                    'success': False,
                    'message': verify_data.get('message', 'Invalid OTP.')
                }), 400
        
        else:
            error_message = 'Invalid OTP. Please try again.'
            try:
                error_data = verify_response.json()
                error_message = error_data.get('message', error_message)
            except:
                pass
            
            return jsonify({
                'success': False,
                'message': error_message
            }), 400
        
    except Exception as e:
        print(f"❌ Verify OTP Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'An error occurred.'}), 500


# =============================================================================
# API: RESEND OTP
# =============================================================================
@app.route('/api/resend-otp', methods=['POST'])
def api_resend_otp():
    """Resend OTP via Django API"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        signup_data = session.get('signup_data')
        login_data = session.get('login_data')
        
        if not email:
            if signup_data:
                email = signup_data.get('email', '')
            elif login_data:
                email = login_data.get('email', '')
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email not found. Please try again.'
            }), 400
        
        print(f"\n🔄 RESENDING OTP to {email}...")
        
        otp_response = requests.post(
            DJANGO_OTP_ENDPOINT,
            json={'email': email},
            headers=DJANGO_HEADERS,
            timeout=DJANGO_TIMEOUT
        )
        
        print(f"Response: {otp_response.status_code}")
        
        if otp_response.status_code in [200, 201]:
            otp_data = otp_response.json()
            if 'otp_id' in otp_data:
                session['otp_id'] = otp_data['otp_id']
            
            return jsonify({
                'success': True,
                'message': f'New OTP sent to {email}'
            }), 200
        
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to resend OTP.'
            }), 400
        
    except Exception as e:
        print(f"❌ Resend OTP Error: {e}")
        return jsonify({'success': False, 'message': 'Failed to resend OTP.'}), 500


# =============================================================================
# RUN APPLICATION
# =============================================================================
if __name__ == '__main__':    
    print('\n\tcaregiver\n')
    app.run(debug=True, port=5003, host='0.0.0.0')