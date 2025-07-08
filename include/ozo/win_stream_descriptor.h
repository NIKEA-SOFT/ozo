#pragma once
#include <boost/asio/ip/tcp.hpp>

namespace ozo::detail {

namespace asio = boost::asio;

struct win_stream_descriptor : asio::ip::tcp::socket {
    using base               = asio::ip::tcp::socket;
    using native_handle_type = base::native_handle_type;

    explicit win_stream_descriptor(asio::io_context& ctx)
        : base(ctx) {}

    explicit win_stream_descriptor(const asio::io_context::executor_type& ex)
        : base(ex) {}

    win_stream_descriptor(asio::io_context& ctx, native_handle_type sock)
        : base(ctx)
    {
        assign(sock);
    }

    win_stream_descriptor(const asio::io_context::executor_type& ex,
                          native_handle_type sock)
        : base(ex)
    {
        assign(sock);
    }

    void assign(native_handle_type sock) {
        base::assign(asio::ip::tcp::v4(), sock);
    }
};

} // namespace ozo::detail
