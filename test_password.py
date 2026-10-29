from werkzeug.security import generate_password_hash

generated_passwod = generate_password_hash("1234")
print(generated_passwod)