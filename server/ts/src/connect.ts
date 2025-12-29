import { Code, ConnectError, type ConnectRouter } from "@connectrpc/connect";
import { PetCodeService, type DecodePetCodeMessageFromBase64Request, type EncodePetCodeMessageToBase64Request } from "@seerbp/petcode-sdk/pb/server/v1/service_pb.js";
import { fromBase64, toBase64 } from "@seerbp/petcode-sdk";
import { PetCodeMessageSchema } from "@seerbp/petcode-sdk/pb/v1/message_pb.js";

export default (router: ConnectRouter) =>
  router.service(PetCodeService, {
    async encodePetCodeMessageToBase64(req: EncodePetCodeMessageToBase64Request) {
      if (!req.petCodeMessage) {
        throw new ConnectError("petCodeMessage is required", Code.InvalidArgument);
      }
      try {
        return {
          base64: toBase64(PetCodeMessageSchema, req.petCodeMessage)
        };
      } catch (error) {
        throw new ConnectError("invalid petCodeMessage", Code.InvalidArgument);
      }
    },
    async decodePetCodeMessageFromBase64(req: DecodePetCodeMessageFromBase64Request) {
      if (!req.base64) {
        throw new ConnectError("base64 is required", Code.InvalidArgument);
      }
      try {
        return {
          petCodeMessage: fromBase64(PetCodeMessageSchema, req.base64)
        };
      } catch (error) {
        throw new ConnectError("invalid base64", Code.InvalidArgument);
      }
    },
  });
