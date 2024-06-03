<template>
    <div id="back">
        <div class="backRight"></div>
        <div class="backLeft"></div>
    </div>

    <div id="slideBox">
        <div class="topLayer">
            <div class="left">
                <SignUp/>
            </div>
            <div class="right">
                <Login />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Sign",
    data() {
        return {
            loading: true
        }
    },
    mounted() {
        this.loading = false
    }
}
</script>
<style>
body {
  height: 100%;
  overflow: hidden;
  width: 100% !important;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.backRight {
  position: absolute;
  right: 0;
  width: 50%;
  height: 100%;
  background: #B5B5B5;
  background-size: cover;
  background-position: 50% 50%;
}

.backLeft {
  position: absolute;
  left: 0;
  width: 50%;
  height: 100%;
  background: #B5B5B5;
  background-size: cover;
  background-position: 50% 50%;
}

#back {
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: -999;
}

#slideBox {
  width: 50%;
  max-height: 100%;
  height: 100%;
  overflow: hidden;
  margin-left: 50%;
  position: absolute;
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
  transition: 0.5s;
}
.topLayer {
  width: 200%;
  height: 100%;
  position: relative;
  left: -100%;
  transition: 0.5s;
  display: flex;
  flex-direction: row;
}

.left {
  width: 50%;
  height: 100%;
  background: var(--surface-0);
  
}

.right {
  width: 50%;
  height: 100%;
  background: var(--surface-0);
}

.marginLeft-0 {
    margin-left: 0!important;
}

.marginLeft-50 {
    margin-left: 50%!important;
}

.marginLeft-100 {
    margin-left: 100%!important;
}


@media screen and (max-width: 966px) {
    #slideBox {
        margin-left: 0;
        width: 100%;
    }

    .topLayer {
        left: -100%
    }
    .left {
        width: 100%;
    }

    .right {
        width: 100%;
    }

    /* .marginLeft-0 {
        margin-left: -100%!important;
    }

    .marginLeft-100 {
        margin-left: 100%!important;
    } */

    .marginLeft-50 {
        margin-left: 0!important;
    }
}
</style>