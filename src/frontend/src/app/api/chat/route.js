export async function POST(req) {
  const { message } = await req.json();
  const defaultResponse = "Chào bạn! Tôi là chatbot, rất vui được trò chuyện với bạn. Bạn khỏe không? Dẫn chứng từ tài liệu: Doc1.pdf";

  // Giả lập streaming bằng cách gửi từng phần của phản hồi
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for (const char of defaultResponse) {
        await new Promise(resolve => setTimeout(resolve, 50)); // Tốc độ streaming: 50ms mỗi ký tự
        controller.enqueue(encoder.encode(char));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain' },
  });
}