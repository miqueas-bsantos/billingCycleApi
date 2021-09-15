import boto3


class Cognito:

    def __init__(self):
        self.cognito = boto3.client('cognito-idp')

    def get_user(self, access_token: str):
        response = {}
        try:
            response = self.cognito.get_user(
                AccessToken=access_token
            )
            response["data"] = response
        except self.cognito.exceptions.InternalErrorException as error:
            response["error"] = {
                "code": 500,
                "type": "/errors/internal-error",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.InvalidParameterException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/invalid-parameter",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.NotAuthorizedException as error:
            response["error"] = {
                "code": 401,
                "type": "/errors/not-authorized",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.PasswordResetRequiredException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/password-reset-required",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.ResourceNotFoundException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/resource-not-found",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.TooManyRequestsException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/too-many-requests",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.UserNotConfirmedException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/user-not-confirmed",
                "message": error.response["Error"]["Message"]
            }
        except self.cognito.exceptions.UserNotFoundException as error:
            response["error"] = {
                "code": 400,
                "type": "/errors/user-not-found",
                "message": error.response["Error"]["Message"]
            }
        except Exception as error:
            response["error"] = {
                "code": 500,
                "type": "/errors/internal-server-error",
                "message": str(error)
            }
        finally:
            return response
