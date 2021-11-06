radio.setGroup(20)
basic.forever(function () {
    radio.sendValue("a", input.temperature())
    radio.sendValue("b", input.lightLevel())
})
