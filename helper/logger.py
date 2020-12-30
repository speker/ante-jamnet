from model.postgre import PostGre
import jwt


class Logger:
    JWT_SECRET = '7n?P3gjjJqDCbgZrS4QD#hz+a83pLrD3rJwdtWbx-K#%jkYf%B_2n$ha$*bY9CUp'
    JWT_ALGORITHM = 'HS256'

    def set_request(self, request):
        user_ip = request.remote_addr
        action_detail = request.json
        if 'token' in action_detail:
            token = action_detail['token']
        print(user_ip)
