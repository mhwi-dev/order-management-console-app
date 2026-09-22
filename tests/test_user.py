import sys
import os

# 1. PHẢI ĐẶT 2 DÒNG NÀY TRÊN CÙNG (Trước các dòng import models, services, repos)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.users import User
from repositories.user_repo import UserRepo
from services.user_service import UserService

# def test_login_flow():
#     # 1. Dùng file JSON test riêng để không đụng tới data thật
#     repo = UserRepo(file_path="data/test_users.json")
#     service = UserService(repo)

#     print("--- ĐANG TEST CHỨC NĂNG ĐĂNG NHẬP ---")

#     # 2. Test Đăng ký
#     user = service.sign_up("huy_test", "123456", "Nguyen Minh Huy", "customer")
#     assert user is not None, "Lỗi: Đăng ký thất bại!"
#     print("✅ Test Đăng ký: PASSED")

#     # 3. Test Đăng nhập đúng pass
#     logged_in = service.login("huy_test", "123456")
#     assert logged_in is not None, "Lỗi: Đúng mật khẩu nhưng không đăng nhập được!"
#     print("✅ Test Đăng nhập đúng pass: PASSED")

#     # 4. Test Đăng nhập sai pass (Mong chờ hệ thống ném ra ValueError)
#     try:
#         service.login("huy_test", "sai_pass")
#         # Nếu dòng trên KHÔNG bị lỗi -> Bài test thất bại!
#         print("❌ Lỗi: Sai mật khẩu nhưng không ném ra ValueError!")
#     except ValueError:
#         # Nếu nhảy vào đây tức là Service đã ném lỗi đúng như thiết kế
#         print("✅ Test Đăng nhập sai pass: PASSED (Đã ném lỗi ValueError chuẩn!)")

def test_get_user_invalid():
    # 1. Dùng file JSON test riêng
    test_file = "data/test_invalid_users.json"
    repo = UserRepo(file_path=test_file)
    service = UserService(repo)

    print("\n--- ĐANG TEST CHỨC NĂNG LỌC USER KHÔNG HỢP LỆ ---")

    # 2. Đảm bảo file test sạch sẽ trước khi chạy
    if os.path.exists(test_file):
        os.remove(test_file)

    # 3. Tạo dữ liệu test thông qua service.sign_up (hoặc ghi dictionary chuẩn)
    # User 1: Hợp lệ
    u1 = service.sign_up("huy_nguyen", "123456", "Nguyen Huy", "customer")
    
    # User 2: Thiếu full_name (tạo user không hợp lệ)
    u2 = service.sign_up("user_loi_1", "123456", "", "customer")
    
    # User 3: Thiếu role
    u3 = service.sign_up("user_loi_2", "123456", "Nguyen Van B", "")

    # 4. Gọi hàm cần test
    invalid_list = service.get_user_invalid()

    # 5. Kiểm tra kết quả (Assert)
    assert len(invalid_list) == 2, f"Lỗi: Kỳ vọng 2 user lỗi nhưng lại ra {len(invalid_list)}"
    
    # Lấy danh sách ID hoặc username để kiểm tra
    invalid_usernames = [u.username for u in invalid_list]
    assert "user_loi_1" in invalid_usernames, "Lỗi: Không lọc được user thiếu full_name"
    assert "user_loi_2" in invalid_usernames, "Lỗi: Không lọc được user thiếu role"
    assert "huy_nguyen" not in invalid_usernames, "Lỗi: User hợp lệ lại bị đưa vào danh sách lỗi"

    print("✅ Test get_user_invalid: PASSED (Lọc chính xác các user thiếu thông tin!)")

if __name__ == "__main__":
    # test_login_flow()
    test_get_user_invalid()