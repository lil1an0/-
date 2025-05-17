<template>
	<div class="home-container">
		<div class="comment-row">
			<label for="commentInput" class="label">输入评论：</label>
			<input
				type="text"
				id="commentInput"
				v-model="commentText"
				class="comment-input"
				placeholder="请输入评论内容"
			/>
		</div>
		<div class="button-container">
			<button @click="submitComment" class="submit-btn">提交</button>
			<button @click="resetComment" class="reset-btn">重置</button>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import * as api from './api';

export default defineComponent({
	name: 'home',
	setup() {
		const commentText = ref('');

		const submitComment = async () => {
			if (!commentText.value.trim()) {
				alert('评论不能为空');
				return;
			}
			try {
				const response = await api.predictObj({ content: commentText.value });
				commentText.value = '';
				alert('情感分析结果为：' + response.data);
			} catch (error) {
				console.error('评论提交失败:', error);
				alert('评论提交失败，请稍后再试');
			}
		};

		const resetComment = () => {
			commentText.value = '';
		};

		return {
			commentText,
			submitComment,
			resetComment,
		};
	},
});
</script>

<style scoped lang="scss">
/* Container for the entire page */
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
}

/* Row for label and input */
.comment-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

/* Styling for the label */
.label {
  font-size: 16px;
  font-weight: bold;
}

/* Styling for the input */
.comment-input {
  padding: 12px; /* 增加内边距 */
  font-size: 16px; /* 增大字体 */
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 600px; /* 更宽 */
  height: 100px; /* 更宽 */
  max-width: 100%;
  box-sizing: border-box;
}

/* Container for buttons */
.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

/* Styling for buttons */
.submit-btn,
.reset-btn {
  padding: 8px 15px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  background-color: #848c84;
  color: white;
}

.submit-btn:hover {
  background-color: #848c84;
}

.reset-btn {
  background-color: #eee2e1;
  color: black;
}

.reset-btn:hover {
  background-color: #eee2e1;
}
</style>
