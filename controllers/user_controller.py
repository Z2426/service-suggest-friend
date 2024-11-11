from flask import Blueprint, request, jsonify
from models.embeddings_model import add_or_update_embedding, search_in_group,get_user_data
from utils.image_utils import load_image_from_url

user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/suggest_friend_by_image', methods=['POST'])
def suggest_friend_by_image():
    data = request.json
    current_user_id = data['userId']  # ID của người dùng hiện tại
    image_url = data['image_url']  # URL của ảnh đầu vào
    print(current_user_id)
    threshold = data.get('threshold', 0.6)  # Ngưỡng độ tương đồng
    # Tải ảnh từ URL
    image = load_image_from_url(image_url)
    if image is not None:
        # Tìm kiếm những người dùng trong ảnh
        detected_users = search_in_group(image, threshold)
        # Lấy dữ liệu của người dùng hiện tại (bạn bè và người bị chặn)
        blocked_users, friends = get_user_data(current_user_id)
        print("Blocked Users:", blocked_users)
        print("Friends:", friends)
        # Lọc ra những người dùng có thể kết bạn (chưa bị chặn và chưa là bạn bè)
        potential_friends = [
            user_id for user_id in detected_users
            if user_id != current_user_id and user_id not in blocked_users and user_id not in friends
        ]
        return jsonify({"suggested_friends": potential_friends}), 200
    else:
        return jsonify({"error": "Could not load image."}), 400
@user_blueprint.route('/add_embedding_2', methods=['POST'])
def add_embedding():
    data = request.json
    user_id = data['user_id']
    image_url = data['image_url']
    image = load_image_from_url(image_url)
    if image is not None:
        response = add_or_update_embedding(user_id, image)
        return jsonify(response), 200
    else:
        return jsonify({"error": "Could not load image."}), 400

@user_blueprint.route('/search_in_group', methods=['POST'])
def search_group():
    data = request.json
    image_url = data['image_url']
    threshold = data.get('threshold', 0.6)
    image = load_image_from_url(image_url)
    if image is not None:
        detected_users = search_in_group(image, threshold)
        return jsonify({"detected_users": detected_users}), 200
    else:
        return jsonify({"error": "Could not load group image."}), 400
