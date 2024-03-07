$(document).ready(function() {
    $('.open-add-sub').click(function() {
        $('#add-sub').show();
    });
    
    
    $(document).on('click', '.close-btn', function() {
        $('.sub').hide();
    });

    $('#add-watchee-form').submit(function(event) {
        event.preventDefault();
        $('#add-sub').hide();
    });

    fetchWatcheeInfo();

    $(document).off('click', '.refresh-btn').on('click', '.refresh-btn', function() {
        var uid = $(this).data('uid');
        refreshContent(uid); 
    });
    $(document).off('click', '.refresh-all').on('click', '.refresh-all', function() {
        refreshContent();
    });

    $(document).on('click', '.view-content-btn', function() {
        var uid = $(this).data('uid');
        fetchWatcheeContent(uid);
    });

    $(document).on('click', '.remove-watchee-btn', function() {
        var uid = $(this).data('uid');
        removeWatchee(uid);
    });
    $(document).on('click', '.refresh-watchee-btn', function() {
        var uid = $(this).data('uid');
        refreshWatchee(uid);
    });
    $('.close-btn').click(function(){
        $('.sub').hide();
    });
});


// 刷新全部订阅作者的内容
function refreshAllWatchees() {
    $.get(baseUrl + "/refresh", function(response) {
        alert('全部内容已刷新!');
        refreshContent();
    }).fail(function() {
        alert("刷新全部内容时发生错误。");
    });
}

// 定义刷新内容的函数
function refreshContent(uid) {
    var url = baseUrl + "/refresh";
    if (uid) {
        url += "?uid=" + uid;
    }
    console.log("refresh "+url);
    $.get(url, function(response) {
        alert(response.message);
        fetchWatcheeInfo();
        // if(response.status === "success") {
        //     alert('内容刷新成功!');
            
        // } else {
            
        // }
    }).fail(function(error) {
        alert("请求失败: " + error.statusText);
    });
}

// 手动刷新作者内容
function refreshWatchee(uid) {
    $.get(baseUrl + "/refresh?uid=" + uid, function(response) {
        alert('作者内容已刷新!');
        refreshContent(uid);
    }).fail(function() {
        alert("刷新作者内容时发生错误。");
    });
}

// 添加订阅
$('#add-watchee-form').submit(function(event){
    event.preventDefault();
    var formData = {
        uid: $("#add-uid").val(),
        platform: $("#platform").val(),
        core: $("#core").val()

    };
    $.ajax({
        type: "POST",
        url: baseUrl + "/add_watchee",
        contentType: "application/json",
        data: JSON.stringify(formData),
        success: function(response) {
            alert('添加订阅成功!');
            $('#add-sub').hide();
            fetchWatcheeInfo();
        },
        error: function(response) {
            alert('添加订阅失败: ' + response.responseJSON.detail);
        }
    });
});


baseUrl = "http://localhost:33200"

// 获取订阅作者信息
function fetchWatcheeInfo() {
    $.get(baseUrl + "/watchee_info", function(data) {
        $(".watchee-list").empty();
        data.forEach(function(item) {
            $(".watchee-list").append(
                `<li>${item.author} (${item.platform} - ${item.core}) - UID: ${item.uid}
                    <div class="button-group">
                        <button class="refresh-btn" data-uid="${item.uid}">刷新</button>
                        <button class="view-content-btn" data-uid="${item.uid}">查看内容</button>
                        <button class="remove-watchee-btn" data-uid="${item.uid}">取消订阅</button>
                    </div>
                </li>`
            );
        });
        $('.view-content-btn').click(function() {
            var uid = $(this).data('uid');
            fetchWatcheeContent(uid);
        });
        $('.remove-watchee-btn').click(function() {
            var uid = $(this).data('uid');
            removeWatchee(uid);
        });
        
    });
}

function getDownloadStatus(status) {
    switch (status) {
        case 0:
            return '<span class="download-status not-downloaded">未下载</span>';
        case 1:
            return '<span class="download-status downloaded">已下载</span>';
        case -1:
            return '<span class="download-status download-failed">下载失败</span>';
        default:
            return '<span class="download-status">未知状态</span>';
    }
}

// 获取订阅作者内容
// TODO: 分页, 懒加载
function fetchWatcheeContent(uid) {
    $.get(baseUrl + "/watchee_content?uid=" + uid, function(data) {
        $("#author-content-list").empty();
        data.forEach(function(item) {
            $("#author-content-list").append(
                `<li>
                    <img src="${item.media_cover}" alt="${item.media_name}" style="max-width: 200px;">
                    <p>简介: <br>${item.media_intro.replace(/\n/g, '<br>')}</p>
                    <p>发布时间: ${new Date(item.media_created * 1000).toLocaleString()}</p>
                    <p>下载状态: ${getDownloadStatus(item.download_status)}</p>
                </li>`
            );
        });
        $("#content-sub").show();
    }).fail(function() {
        alert("请求订阅作者内容时发生错误。");
    });
}


// 取消订阅
function removeWatchee(uid) {
    if (confirm("是否删除已下载的文件")) {
        var formData = {
            uid: uid,
            delete_medias: true
        };
    } else {
        var formData = {
            uid: uid,
            delete_medias: false
        };
    }
    
    $.ajax({
        type: "POST",
        url: baseUrl + "/remove_watchee",
        contentType: "application/json",
        data: JSON.stringify(formData),
        success: function(response) {
            alert('取消订阅成功!');
            fetchWatcheeInfo();
        },
        error: function(response) {
            alert('取消订阅失败: ' + response.responseJSON.detail);
        }
    });
}
