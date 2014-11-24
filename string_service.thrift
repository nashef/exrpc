/* A Simple Example RPC Service using Thrift
 */

struct StringMessage {
    1: required string content;
    2: optional i32 times;
}

service StringService {
    string echo(1:StringMessage input);
}
